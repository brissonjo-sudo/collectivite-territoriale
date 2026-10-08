[CmdletBinding()]
param([switch]$ControleSeulement)

# Utiliser un terminal indépendant après fermeture complète de Codex.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$runtimeCampagne = 'C:\Users\Krn\AppData\Local\OpenAI\Codex\runtimes\cua_node\3dd31cfff853001c\bin\node_repl.exe'
$candidatsCampagne = @(Get-CimInstance Win32_Process -Filter "Name='node_repl.exe'" -ErrorAction Stop)
if (@($candidatsCampagne | Where-Object { -not $_.ExecutablePath }).Count -gt 0) {
    throw 'Chemin de processus inaccessible : aucune sonde ni campagne lancée.'
}
$processusCampagne = @($candidatsCampagne | Where-Object {
    $_.ExecutablePath -and [string]::Equals($_.ExecutablePath, $runtimeCampagne, [StringComparison]::OrdinalIgnoreCase)
})
if ($processusCampagne.Count -gt 0) {
    Write-Host "Runtime Codex encore actif (PID : $(($processusCampagne | Select-Object -ExpandProperty ProcessId) -join ', '))."
    Write-Host 'Fermer Codex complètement, conserver le terminal indépendant ouvert et relancer cette commande.'
    Write-Host 'Aucune sonde, aucun setup et aucune campagne lancés.'
    exit 2
}

$manifestCampagne = Join-Path $PSScriptRoot 'qualification-coactivation-dev7-cli-r3\manifest.json'
if (-not (Test-Path -LiteralPath $manifestCampagne -PathType Leaf)) {
    throw 'Manifest préparé absent. Aucune préparation, installation ou campagne lancée.'
}
$pythonCampagne = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $pythonCampagne -PathType Leaf)) {
    $pythonCampagne = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
}
if (-not (Test-Path -LiteralPath $pythonCampagne -PathType Leaf)) { throw 'Python de qualification introuvable.' }
$scriptCampagne = Join-Path $PSScriptRoot 'executer_campagne_dev7_hors_codex_20261008.py'
if (-not (Test-Path -LiteralPath $scriptCampagne -PathType Leaf)) { throw 'Harnais hors application absent.' }
$env:PYTHONUTF8 = '1'
if ($ControleSeulement) {
    & $pythonCampagne $scriptCampagne --controle-seulement
} else {
    Write-Host 'Une lecture réelle sans modèle précède les trois tentatives uniques, puis leurs exports.'
    Write-Host 'Durée maximale du harnais : environ 15 minutes. Aucun setup ni nouvelle authentification.'
    & $pythonCampagne $scriptCampagne
}
exit $LASTEXITCODE
