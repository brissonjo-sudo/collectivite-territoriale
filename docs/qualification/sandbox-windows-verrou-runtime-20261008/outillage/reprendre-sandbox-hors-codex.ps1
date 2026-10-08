[CmdletBinding()]
param([switch]$ControleSeulement)

# Une vérification des processus précède la reprise officielle, sans arrêt forcé.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$runtimeBloqueSandbox = Join-Path $env:LOCALAPPDATA 'OpenAI\Codex\runtimes\cua_node\3dd31cfff853001c\bin\node_repl.exe'
$candidatsSandbox = @(Get-CimInstance Win32_Process -Filter "Name='node_repl.exe'" -ErrorAction Stop)
if (@($candidatsSandbox | Where-Object { -not $_.ExecutablePath }).Count -gt 0) {
    throw 'Chemin de certains processus inaccessible : précontrôle non confirmé. Aucune tentative de setup lancée.'
}
$processusSandbox = @($candidatsSandbox |
    Where-Object { $_.ExecutablePath -and [string]::Equals($_.ExecutablePath, $runtimeBloqueSandbox, [StringComparison]::OrdinalIgnoreCase) })
if ($processusSandbox.Count -gt 0) {
    $identifiantsSandbox = ($processusSandbox | Select-Object -ExpandProperty ProcessId) -join ', '
    Write-Host "Runtime encore utilisé par $($processusSandbox.Count) processus (PID : $identifiantsSandbox)."
    Write-Host 'Fermer Codex complètement et conserver ce terminal PowerShell ouvert, puis relancer cette commande.'
    Write-Host 'Aucun processus arrêté et aucune tentative de setup lancée.'
    exit 2
}
Write-Host 'Aucun processus actif trouvé pour le runtime qui a bloqué la tentative précédente.'
Write-Host 'Ce précontrôle ne garantit pas la réussite du setup ni de la lecture.'
if ($ControleSeulement) { exit 0 }
$repriseSandbox = Join-Path $PSScriptRoot 'reprendre-sandbox-isole.ps1'
if (-not (Test-Path -LiteralPath $repriseSandbox -PathType Leaf)) { throw 'Lanceur de reprise isolée absent.' }
& $repriseSandbox
