resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-db-state-locks" # Name of the DynamoDB table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Environment = "prod"
    Name        = "Terraform-db-StateLocks"
  }
}