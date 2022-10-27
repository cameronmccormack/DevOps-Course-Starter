terraform {
  required_providers {
    azurerm = {
      source    = "hashicorp/azurerm"
      version   = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "Softwire21_CameronMcCormack_ProjectExercise"
    storage_account_name = "tfstate1a2b3"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name  = "Softwire21_CameronMcCormack_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                  = "terraformed-asp"
  location              = data.azurerm_resource_group.main.location
  resource_group_name   = data.azurerm_resource_group.main.name
  os_type               = "Linux"
  sku_name              = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                  = "${var.prefix}-todo-app"
  location              = data.azurerm_resource_group.main.location
  resource_group_name   = data.azurerm_resource_group.main.name
  service_plan_id       = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image      = "cameronmccormack/todo-app"
      docker_image_tag  = "latest"
    }
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"    = "https://index.docker.io"
    "GITHUB_CLIENT_ID"              = "${var.github_client_id}"
    "GITHUB_CLIENT_SECRET"          = "${var.github_secret}"
    "DB_PRIMARY_CONNECTION_STRING"  = azurerm_cosmosdb_account.main.connection_strings[0]
    "DB_NAME"                       = azurerm_cosmosdb_mongo_database.main.name
    "SECRET_KEY"                    = "${var.flask_secret}"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmos-db-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level = "BoundedStaleness"
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }

}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-cosmos-mongo-db"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
}
