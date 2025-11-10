# Terraform Variables assignment for the Medical Context RAG deployment
# Copy this file to terraform.tfvars and customize the values for your environment

# Core Configuration
organization_prefix = "MedRag"  # all your resources will be prefixed with this value
environment         = "dev"    # make sure it matches with the terraform workspace you set
location            = "westus3"

# Additional SFI tags for all resources
additional_tags = {
  "Lifecycle"   = "dev"
  "CreatedDate" = "2025-11-09"
  "CreatedBy"   = "paulwu@onemtc.net"
  "Owner"       = "paulwu@onemtc.net"
  "RGMonthlyCost" = "1"
}

# Deployment Flags
deploy_infrastructure = true
deploy_private_network = false  # Set to true will cause Container App Environment to use a premium SKU
deploy_ai_foundry_instances = true
deploy_ai_model_deployments = true
deploy_container_app_environment = true  # Azure Front Door will not be created when set to false
deploy_container_app_helloworld = true    # ignored if deploy_container_app_environment is false
destroy_ai_foundry_instances = false      # explicit setting to destroy AI Foundry instances

# Log Analytics Configuration
use_existing_log_analytics                 = true
existing_log_analytics_workspace_name      = "onemtcww"
existing_log_analytics_resource_group_name = "onemtcww-oms"
log_analytics_subscription_id              = "595a74d5-5d8a-421d-b364-979ba24a6489" # Leave empty if same subscription, or specify different subscription ID

# Key Vault Configuration
key_vault_sku                       = "standard"
key_vault_certificate_contact_email = "paul.wu@microsoft.com"
key_vault_certificate_contact_name  = "Paul Wu"
key_vault_certificate_contact_phone = "714-679-5388"

# Storage Account Configuration
storage_account_tier             = "Standard"
storage_account_replication_type = "LRS"

# Cosmos DB Configuration
cosmos_db_consistency_level = "Session"
cosmos_db_database_id             = "medical-ctx-rag"  # don't change this value

cosmos_db_containers = [
    {
      name          = "Configuration1"
      partition_key = "/id"
      throughput    = 400
    },
    {
      name          = "Configuration2"
      partition_key = "/id"
      throughput    = 400
    }
]


# Container App Configuration
container_app_image = "nginxdemos/hello:latest"
#container_app_image        = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
container_app_cpu          = 0.25
container_app_memory       = "0.5Gi"
container_app_min_replicas = 1
container_app_max_replicas = 10
container_app_target_port  = 80

# Container Registry Configuration
container_registry_sku           = "Basic"
container_registry_admin_enabled = true

# AI Foundry Configuration
aif_location1 = "eastus2"

