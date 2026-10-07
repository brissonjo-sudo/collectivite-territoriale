# Lancement manuel après vérification de la connexion juridique.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PluginRoot,
    [string]$Python = 'C:\Users\Krn\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe',
    [string]$Claude = 'C:\Users\Krn\.local\bin\claude.exe',
    [string]$Revision = 'r8'
)
$ErrorActionPreference = 'Stop'
if ($Revision -notmatch '^r[0-9]+$') { throw 'Révision invalide.' }
$NotBefore = [DateTimeOffset]::Parse('2026-10-07T01:31:00Z')
if ([DateTimeOffset]::UtcNow -lt $NotBefore) {
    throw 'Attendre le 7 octobre 2026 à 03 h 31 Europe/Paris. Ce script ne programme aucune tâche.'
}
$Root = (Resolve-Path -LiteralPath $PluginRoot).Path
foreach ($Executable in @($Python, $Claude)) {
    if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) { throw "Exécutable absent : $Executable" }
}
$Evidence = Join-Path $Root 'tests\evidence\coactivation-corrigee'
$Manifest = Join-Path $Evidence "gel-$Revision.json"
$Output = Join-Path $Evidence "campagne-$Revision"
if ((Test-Path -LiteralPath $Manifest) -or (Test-Path -LiteralPath $Output)) {
    throw 'Gel ou dossier de mesure existant : choisir une nouvelle révision. Aucun écrasement.'
}
$Reference = Get-Content -LiteralPath (Join-Path $Evidence 'gel-dev4.json') -Raw | ConvertFrom-Json
foreach ($Entry in $Reference.files.PSObject.Properties) {
    $Source = Join-Path $Root $Entry.Name
    if ((Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Entry.Value) {
        throw "Runtime, harnais ou suite différents du candidat dev.4 : $($Entry.Name). Qualifier ce changement séparément."
    }
}
$PreviousUtf8 = $env:PYTHONUTF8
$env:PYTHONUTF8 = '1'
Push-Location -LiteralPath $Root
try {
    & $Python 'scripts\freeze_corrected_candidate.py' --output $Manifest
    if ($LASTEXITCODE -ne 0) { throw 'Gel refusé : runtime non committé ou divergent.' }
    $Cases = Get-Content -LiteralPath 'tests\cas-coactivation-v2.json' -Raw | ConvertFrom-Json
    $AttemptCount = 0
    foreach ($Case in $Cases) {
        & $Python -u 'scripts\run_corrected_campaign.py' --claude $Claude --frozen-manifest $Manifest --output-dir $Output --case $Case.id
        $TechnicalExit = $LASTEXITCODE
        $AttemptCount++
        Write-Host "$($Case.id) : code technique $TechnicalExit ; aucun verdict comportemental déduit."
        $Trace = Join-Path $Output "$($Case.id).jsonl"
        if (Test-Path -LiteralPath $Trace -PathType Leaf) {
            $Events = @(Get-Content -LiteralPath $Trace | ForEach-Object { $_ | ConvertFrom-Json })
            $Results = @($Events | Where-Object { $_.type -eq 'result' })
            if ($Results.Count -eq 1 -and $Results[0].is_error -eq $true -and $Results[0].result -match "^You've hit your session limit") {
                Write-Warning 'Quota toujours actif : arrêt de la tentative. Traces conservées ; nouvelle révision requise pour une reprise.'
                break
            }
            $UnavailableMcp = @($Events | Where-Object {
                $_.type -eq 'technical_assessment' -and 'mcp_not_connected' -in $_.failures
            })
            if ($Case.mcp_mode -eq 'required' -and $UnavailableMcp.Count -gt 0) {
                Write-Warning 'MCP juridique non connecté : arrêt des appels nominaux. Réauthentifier avec /mcp, puis choisir une nouvelle révision. Réponse conservée pour jugement indépendant.'
                break
            }
        }
    }
    Write-Host "$AttemptCount tentatives conservées. Chaque réponse complète doit encore recevoir un jugement indépendant frais."
} finally {
    Pop-Location
    $env:PYTHONUTF8 = $PreviousUtf8
}
