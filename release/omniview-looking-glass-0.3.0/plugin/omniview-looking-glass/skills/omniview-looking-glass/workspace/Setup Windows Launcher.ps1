# Creates only this portable workspace's shortcut and folder-icon binding.
[CmdletBinding()]
param()
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$workspaceRoot=(Get-Item -LiteralPath $PSScriptRoot).FullName
$entryPath=Join-Path $workspaceRoot 'host.py'
$iconPath=Join-Path $workspaceRoot 'native\omniview.ico'
$launchPath=Join-Path $workspaceRoot 'Launch OmniView.ps1'
$shortcutPath=Join-Path $workspaceRoot 'OmniView.lnk'
$folderIconPath=Join-Path $workspaceRoot 'desktop.ini'
foreach($requiredPath in @($entryPath,$iconPath,$launchPath)) {
    if(-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {throw 'OmniView launcher payload is incomplete; no binding was written.'}
}
foreach($ownedPath in @($workspaceRoot,$shortcutPath,$folderIconPath)) {
    if((Test-Path -LiteralPath $ownedPath) -and ((Get-Item -LiteralPath $ownedPath -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {throw 'Refusing a linked launcher or folder-icon target.'}
}
$windowsShell=Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
if(-not (Test-Path -LiteralPath $windowsShell -PathType Leaf)) {throw 'Windows PowerShell is unavailable; no binding was written.'}
# The Unicode shell-link interface preserves non-ASCII extraction paths.
if(-not ('OmniView.NativeShortcut' -as [type])) { Add-Type -Path (Join-Path $workspaceRoot 'native\ShellLink.cs') }
$launchArguments='-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "'+$launchPath+'"'
[OmniView.NativeShortcut]::Create($shortcutPath,$windowsShell,$launchArguments,$workspaceRoot,$iconPath,'OmniView - The Looking Glass camera')
if(Test-Path -LiteralPath $folderIconPath) { [IO.File]::SetAttributes($folderIconPath,[IO.FileAttributes]::Normal) }
$folderMetadata=if(Test-Path -LiteralPath $folderIconPath) {[IO.File]::ReadAllText($folderIconPath)} else {''}
$iconSectionPattern='(?ims)^\[\.ShellClassInfo\]\r?\n(?<body>.*?)(?=^\[|\z)'
$sectionUpdate=[Text.RegularExpressions.MatchEvaluator]{param($sectionMatch)
    $retainedLines=@($sectionMatch.Groups['body'].Value -split '\r?\n' | Where-Object {$_ -notmatch '^\s*(IconResource|IconFile|IconIndex)\s*=' -and $_.Length -gt 0})
    return "[.ShellClassInfo]`r`nIconResource=native\omniview.ico,0`r`n"+($retainedLines -join "`r`n")+"`r`n"
}
if([regex]::IsMatch($folderMetadata,$iconSectionPattern)) {$folderMetadata=[regex]::Replace($folderMetadata,$iconSectionPattern,$sectionUpdate)}
else {$folderMetadata=$folderMetadata.TrimEnd()+"`r`n[.ShellClassInfo]`r`nIconResource=native\omniview.ico,0`r`n"}
[IO.File]::WriteAllText($folderIconPath,$folderMetadata,[Text.UnicodeEncoding]::new($false,$true))
[IO.File]::SetAttributes($folderIconPath,[IO.FileAttributes]::Hidden -bor [IO.FileAttributes]::System)
$folderAttributes=[IO.File]::GetAttributes($workspaceRoot)
[IO.File]::SetAttributes($workspaceRoot,$folderAttributes -bor [IO.FileAttributes]::ReadOnly)
[ordered]@{configured=$true;root=$workspaceRoot;shortcut=$shortcutPath;icon=$iconPath;storage_modified=$false} | ConvertTo-Json -Compress
