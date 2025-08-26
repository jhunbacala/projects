# main.tf file 

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_ssm_parameter" "db_password" {
  name        = "/demo/db_password"
  type        = "SecureString"
  value       = var.db_password
  overwrite   = true
}
