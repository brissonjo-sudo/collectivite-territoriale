# Reprise manuelle à froid ; aucune fermeture, authentification ou configuration.
[CmdletBinding()]
param([switch]$ControleSeulement)
$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\Krn\Documents\Codex\2026-10-06\reprends-le-travail-de-cette-session'
$taskPython = 'C:\Users\Krn\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$taskHarness = Join-Path $taskRoot 'campagne_native_complete_dev7_20261009_r3.py'
$taskRun = Join-Path $taskRoot 'qualification-coactivation-dev7-complet-20261009-r3'
$taskLog = Join-Path $taskRoot ('reprise-complete-dev7-r3-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8) + '.local.txt')
if (-not (Test-Path -LiteralPath $taskPython -PathType Leaf)) { throw 'Python attendu absent.' }
if (-not (Test-Path -LiteralPath $taskHarness -PathType Leaf)) { throw 'Harnais attendu absent.' }
if (Test-Path -LiteralPath $taskLog) { throw 'Journal existant ; aucun remplacement.' }
$taskCuaBin = 'C:\Users\Krn\AppData\Local\OpenAI\Codex\runtimes\cua_node\3dd31cfff853001c\bin'
$taskNodeTargets = @((Join-Path $taskCuaBin 'node.exe'), (Join-Path $taskCuaBin 'node_repl.exe'))
$taskLogBytes = 0
$taskLogLimit = 65536
$taskEncoding = [Text.UTF8Encoding]::new($false)
$taskInitialBytes = $taskEncoding.GetBytes("Reprise native complète : $(Get-Date -Format o)`r`n")
$taskLogStream = [IO.File]::Open($taskLog, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
try { $taskLogStream.Write($taskInitialBytes,0,$taskInitialBytes.Length) } finally { $taskLogStream.Dispose() }
try {
  $taskNodes = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('node.exe', 'node_repl.exe') })
  if (@($taskNodes | Where-Object { -not $_.ExecutablePath }).Count -gt 0) { throw 'Chemin CIM inaccessible ; aucun lancement.' }
  if (@($taskNodes | Where-Object { $_.ExecutablePath -in $taskNodeTargets }).Count -gt 0) { throw 'Runtime CUA encore actif : fermer complètement Codex et relancer à froid. Aucun processus terminé.' }
} catch {
  [IO.File]::AppendAllText($taskLog, "Précontrôle CIM bloqué : $($_.Exception.Message)`r`n", $taskEncoding)
  throw
}
function Invoke-TaskHarness {
  param([string]$TaskAction)
  $taskArguments = @('-B', $taskHarness, $TaskAction, '--run', $taskRun)
  if ($TaskAction -in @('prepare', 'run-all')) { $taskArguments += '--offline' }
  & $taskPython @taskArguments 2>&1 | ForEach-Object {
    $taskLine = [string]$_
    $taskLineBytes = $taskEncoding.GetByteCount($taskLine + "`r`n")
    if (($script:taskLogBytes + $taskLineBytes) -le $script:taskLogLimit) {
      [IO.File]::AppendAllText($script:taskLog, $taskLine + "`r`n", $script:taskEncoding)
      $script:taskLogBytes += $taskLineBytes
      Write-Output $taskLine
    }
  }
  if ($LASTEXITCODE -ne 0) { throw "Étape $TaskAction bloquée (code $LASTEXITCODE). Preuves conservées : $taskLog" }
}
$taskPreviousUtf8 = [Environment]::GetEnvironmentVariable('PYTHONUTF8','Process')
$taskPreviousBytecode = [Environment]::GetEnvironmentVariable('PYTHONDONTWRITEBYTECODE','Process')
try {
  $env:PYTHONUTF8 = '1'
  $env:PYTHONDONTWRITEBYTECODE = '1'
  Set-Location -LiteralPath $taskRoot
  Invoke-TaskHarness 'check'
  if ($ControleSeulement) {
    Write-Output "Contrôle statique terminé ; aucun préflight source ni modèle. Journal : $taskLog"
  } else {
    Invoke-TaskHarness 'prepare'
    Invoke-TaskHarness 'run-all'
    Write-Output "Réponses/exports conservés ; aucun juge créé ici, aucune revue humaine simulée. Journal : $taskLog"
  }
} finally {
  [Environment]::SetEnvironmentVariable('PYTHONUTF8',$taskPreviousUtf8,'Process')
  [Environment]::SetEnvironmentVariable('PYTHONDONTWRITEBYTECODE',$taskPreviousBytecode,'Process')
}
