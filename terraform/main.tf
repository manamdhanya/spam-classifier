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
  default     = 8502
}

variable "metrics_port" {
  description = "Host port for Prometheus metrics"
  type        = number
  default     = 8001
}

provider "docker" {}

resource "docker_image" "app" {
  name = "spam-streamlit:1.0"
  build {
    context = ".."
  }
}

resource "docker_container" "app" {
  name  = "spam-streamlit-terraform"
  image = docker_image.app.image_id
  ports {
    internal = 8501
    external = var.ui_port
  }
  ports {
    internal = 8000
    external = var.metrics_port
  }
}

output "ui_url" {
  value = "http://localhost:${var.ui_port}"
}

output "metrics_url" {
  value = "http://localhost:${var.metrics_port}/metrics"
}
