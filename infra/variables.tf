variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "rg-ticket-api"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "northeurope"
}

variable "app_name_suffix" {
  description = "Suffix for the app name to ensure uniqueness"
  type        = string
  default     = "dev"
}
