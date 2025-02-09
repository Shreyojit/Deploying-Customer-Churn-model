data "google_container_engine_versions" "default" {
  location = "asia-south1-a"
}

resource "google_container_cluster" "default" {
  name               = "flask-cluster"
  location           = "asia-south1-a"
  initial_node_count = 2
  min_master_version = data.google_container_engine_versions.default.latest_master_version

  node_config {
    machine_type = "e2-small"
    disk_size_gb = 30
  }

  # Graceful deletion delay
  provisioner "local-exec" {
    when    = destroy
    command = "sleep 90"
  }
}