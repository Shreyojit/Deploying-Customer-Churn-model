terraform {
  required_version = ">= 1.0"
  backend "gcs" {
    # Bucket name will be provided via GitHub Secrets (GCP_TF_STATE_BUCKET)
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "kubernetes" {
  host  = google_container_cluster.default.endpoint
  token = data.google_client_config.current.access_token

  client_certificate     = base64decode(google_container_cluster.default.master_auth[0].client_certificate)
  client_key             = base64decode(google_container_cluster.default.master_auth[0].client_key)
  cluster_ca_certificate = base64decode(google_container_cluster.default.master_auth[0].cluster_ca_certificate)
}

data "google_client_config" "current" {}