# Launch this exact portable camera; records remain outside its installation.
[CmdletBinding()]
param([switch]$NoBrowser,[string]$DataHome)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$hostPath=Join-Path $PSScriptRoot 'host.py'
if(-not (Test-Path -LiteralPath $hostPath -PathType Leaf)) {throw 'Keep the complete OmniView workspace together; host.py is missing.'}
$pythonCommand=Get-Command py -ErrorAction SilentlyContinue
$pythonArguments=@()
if($pythonCommand) {$pythonArguments+= '-3'} else {$pythonCommand=Get-Command python -ErrorAction SilentlyContinue}
if(-not $pythonCommand) {throw 'Install Python 3.10 or newer, then open OmniView again.'}
$pythonArguments+= $hostPath
if($NoBrowser) {$pythonArguments+= '--no-browser'}
if($DataHome) {$pythonArguments+= @('--data-home',$DataHome)}
& $pythonCommand.Source @pythonArguments 1>$null
if($LASTEXITCODE -ne 0) {throw 'OmniView could not open. See the host error or workspace.log in your data folder.'}
