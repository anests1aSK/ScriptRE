$service = Get-Service -Name "NombreDelServicioEDR"
if ($service.Status -ne "Running") {
    Send-MailMessage -From "alertas@empresa.com" -To "admin@empresa.com" -Subject "Servicio EDR Desactivado" -Body "El servicio EDR ha sido desactivado en el sistema."
    Add-Content -Path "C:\Logs\EDRMonitor.log" -Value "[$(Get-Date)] - Servicio EDR desactivado."
} else {
    Add-Content -Path "C:\Logs\EDRMonitor.log" -Value "[$(Get-Date)] - Servicio EDR en funcionamiento: $($service.Status)"
}