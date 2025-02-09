variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "container_image" {
  description = "Docker image URL (e.g., docker.io/yourusername/flask-app:tag)"
  default     = "asia-south1"
}