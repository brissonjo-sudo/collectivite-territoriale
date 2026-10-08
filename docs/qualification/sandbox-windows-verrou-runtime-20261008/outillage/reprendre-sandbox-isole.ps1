[CmdletBinding()]
param()

# Une invocation utilisateur = une tentative nouvelle et conservée.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$scriptRootSandbox = [IO.Path]::GetFullPath($PSScriptRoot)
$commandSandbox = Get-Command codex.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if ($commandSandbox) {
    $cliPathSandbox = $commandSandbox.Source
} else {
    $binRootSandbox = Join-Path $env:LOCALAPPDATA 'OpenAI\Codex\bin'
    $candidateSandbox = Get-ChildItem -LiteralPath $binRootSandbox -Directory -ErrorAction Stop |
        Sort-Object LastWriteTime -Descending |
        ForEach-Object { Join-Path $_.FullName 'codex.exe' } |
        Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
        Select-Object -First 1
    if (-not $candidateSandbox) { throw "codex.exe introuvable dans PATH et le dossier de l'application." }
    $cliPathSandbox = $candidateSandbox
}
$pythonPathSandbox = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $pythonPathSandbox -PathType Leaf)) {
    $pythonPathSandbox = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
}
if (-not (Test-Path -LiteralPath $pythonPathSandbox -PathType Leaf)) { throw 'Python local introuvable.' }
Write-Host 'Configuration du sandbox Windows isolé ; aucune inférence modèle.'
Write-Host "Valider l'invite administrateur UAC si Windows l'affiche."
& $pythonPathSandbox (Join-Path $scriptRootSandbox 'reprendre_sandbox_isole_20261008.py') --cli $cliPathSandbox
if ($LASTEXITCODE -ne 0) { throw "Configuration ou lecture non confirmée (code $LASTEXITCODE). Les preuves sont conservées." }
