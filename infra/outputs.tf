output "app_url" {
  description = "The default URL of the deployed web app"
  value       = azurerm_linux_web_app.app.default_hostname
}
