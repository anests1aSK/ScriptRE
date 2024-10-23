$imps = ls "$env:WinDir\*.exe" | ForEach-Object {
    Get-Win32ModuleImport -Path $_.FullName
}
$imps | Where-Object Names -Contains "CreateProcessW" |
Select-Object ModulePath