# Configure the Google Cloud provider
provider "google" {
  project = "caramel-clover-461405-f6" # <-- TODO: Replace with your GCP Project ID
  region  = "us-central1"
  zone    = "us-central1-a"
}

# Define the GCP Compute Engine instance
resource "google_compute_instance" "gemini_vm" {
  name         = "gemini-vm-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  # Define the boot disk and image
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      labels = {
        "created-by" = "gemini-cli"
      }
    }
  }

  # Configure the network interface
  # This uses the 'default' VPC network and assigns an ephemeral public IP.
  network_interface {
    network = "default"
    access_config {
      // Ephemeral IP
    }
  }

  # Add some metadata and tags
  metadata = {
    "created-by" = "gemini-cli"
  }
  tags = ["web-server", "dev"]

  # Example startup script to install a simple web server
  metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y nginx
    echo "<html><body><h1>Hello from your Gemini-created VM!</h1></body></html>" | sudo tee /var/www/html/index.html
  EOT

  # Allow HTTP traffic
  allow_stopping_for_update = true
}

# Output the instance name
output "instance_name" {
  description = "The name of the created VM instance."
  value       = google_compute_instance.gemini_vm.name
}

# Output the external IP address of the instance
output "instance_external_ip" {
  description = "The external IP address of the VM instance."
  value       = google_compute_instance.gemini_vm.network_interface[0].access_config[0].nat_ip
}

# Output the internal IP address of the instance
output "instance_internal_ip" {
  description = "The internal IP address of the VM instance."
  value       = google_compute_instance.gemini_vm.network_interface[0].network_ip
}
