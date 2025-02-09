output "load_balancer_ip" {
  value = google_compute_address.default.address
}

output "cluster_endpoint" {
  value = google_container_cluster.default.endpoint
}