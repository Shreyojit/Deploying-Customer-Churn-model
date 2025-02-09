resource "kubernetes_deployment" "flask" {
  metadata {
    name = "flask-deployment"
    labels = {
      app = "flask"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "flask"
      }
    }

    template {
      metadata {
        labels = {
          app = "flask"
        }
      }

      spec {
        container {
          name  = "flask-container"
          image = var.container_image
          port {
            container_port = 5000  # Matches Flask's port
          }
        }
      }
    }
  }
}

resource "google_compute_address" "default" {
  name   = "flask-service-ip"
  region = var.region
}

resource "kubernetes_service" "flask" {
  metadata {
    name = "flask-service"
  }

  spec {
    type             = "LoadBalancer"
    load_balancer_ip = google_compute_address.default.address
    
    external_traffic_policy = "Local"
     
    port {
      port        = 80        # External port
      target_port = 5000      # Internal port (Flask)
    }

    selector = {
      app = "flask"
    }
  }
}