resource "aws_db_subnet_group" "subnet_group" {
  name        = "${var.db_name}-subnet-group-${random_integer.random_suffix.result}"
  description = "Subnet group for ${var.db_name} RDS"
  subnet_ids  = [
    aws_subnet.private-subnet[0].id,
    aws_subnet.private-subnet[1].id
  ]
  tags = {
    Name = "${var.db_name}-subnet-group"
  }
}


resource "aws_db_instance" "primary" {
  identifier               = "${var.db_name}-db"
  engine                   = "postgres"
  engine_version           = var.engine_version
  instance_class           = var.instance_class
  allocated_storage        = var.allocated_storage
  db_name                  = var.db_name
  username                 = var.username
  password                 = var.password
  db_subnet_group_name     = aws_db_subnet_group.subnet_group.name
  vpc_security_group_ids   = [aws_security_group.rds.id]

  skip_final_snapshot      = true
  deletion_protection      = false
  backup_retention_period  = 7
  backup_window            = "02:00-03:00"
  maintenance_window       = "sun:04:00-sun:05:00"
  publicly_accessible      = false
  multi_az                 = true
  storage_encrypted        = true
  auto_minor_version_upgrade = true
  monitoring_interval      = 60
  monitoring_role_arn      = aws_iam_role.rds_monitoring_role.arn

  tags = {
    Name        = "${var.db_name}-rds"
    Environment = var.environment
  }
}
