$key = New-NtKey -Win32Path "HKCU\SOFTWARE\ABC"
Set-NtKeyValue -Key $key -Name "`0HIDDEN" -String "HELLO"
function Select-HiddenValue {
    [CmdletBinding()]
    param(
        [parameter(ValueFromPipeline)]
        $Key
    )

    Process {
       foreach($val in $Key.Values) {
            if ($val.Name -match "`0") {
                [PSCustomObject]@{
                    RelativePath = $Key.RelativePath
                    Name = $val.Name
                    Value = $val.DataObject
                }
            }
        }
    }
}
ls -Recurse NtKeyUser:\SOFTWARE | Select-HiddenValue | Format-Table


Remove-NtKey $key
$key.Close()