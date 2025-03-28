terraform {
  backend "s3" {
    bucket         = "temperature-bucket-1"
    key            = "backend-db/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-db-state-locks"
    encrypt        = true
  }
}