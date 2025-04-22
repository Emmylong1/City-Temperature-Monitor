resource "aws_db_subnet_group" "subnet_group" {
  name        = "${var.db_name}-subnet-group"
  description = "Subnet group for ${var.db_name} RDS"
  subnet_ids  = data.aws_subnets.private.ids

  tags = {
    Name = "${var.db_name}-subnet-group"
  }
}

# Reference to the AWS Secrets Manager secret containing the DB password
data "aws_secretsmanager_secret" "db_password" {
  name = "mydb-password"  # The name of the secret you created in AWS Secrets Manager
}

data "aws_secretsmanager_secret_version" "db_password_version" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}

resource "aws_db_instance" "primary" {
  identifier               = "${var.db_name}-db"
  engine                   = "postgres"
  engine_version           = var.engine_version
  instance_class           = var.instance_class
  allocated_storage        = var.allocated_storage
  db_name                  = var.db_name
  username                 = jsondecode(data.aws_secretsmanager_secret_version.db_password_version.secret_string)["username"]
  password                 = jsondecode(data.aws_secretsmanager_secret_version.db_password_version.secret_string)["password"]
  db_subnet_group_name     = aws_db_subnet_group.subnet_group.name
  vpc_security_group_ids   = [aws_security_group.rds.id]

  skip_final_snapshot      = true
  deletion_protection      = true
  backup_retention_period  = 7
  backup_window            = "02:00-03:00"
  maintenance_window       = "sun:04:00-sun:05:00"
  publicly_accessible      = false
  multi_az                 = true
  storage_encrypted        = true
  auto_minor_version_upgrade = true
  monitoring_interval      = 60

  tags = {
    Name        = "${var.db_name}-rds"
    Environment = var.environment
  }
}