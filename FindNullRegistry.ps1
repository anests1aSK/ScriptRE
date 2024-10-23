$key = New-NtKey -Win32Path "HKCU\SOFTWARE\`0HIDDENKEY"
ls NtKeyUser:\SOFTWARE -Recurse | Where-Object Name -Match "`0"