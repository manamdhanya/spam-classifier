
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

variable "ui_port" {
  description = "Host port for Streamlit"
  type        = number
  default     = 8503
}

provider "docker" {}

data "docker_image" "app" {
  name = "sms-spam-classifier:v1"
}

resource "docker_container" "app" {
  name  = "sms-spam-terraform"
  image = data.docker_image.app.id

  ports {
    internal = 8501
    external = var.ui_port
  }
}

output "ui_url" {
  value = "http://localhost:${var.ui_port}"
}
