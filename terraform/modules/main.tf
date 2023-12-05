##############
## TF State ##
##############

terraform {
  backend "s3" {
    bucket = "terraform-state-09-12-2023-bu-cs673"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

###################
## ACM Resources ##
###################

#resource "aws_acm_certificate" "domain_cert" {
#  domain_name       = "bumtelevision.com"
#  validation_method = "EMAIL"
#
#  tags = {
#    Environment = "flask-app-cert"
#  }
#
#  lifecycle {
#    create_before_destroy = true
#  }
#}

###################
## ALB Resources ##
###################

resource "aws_lb" "flask_app_alb" {
  name               = "flask-app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.flask_app_sg.id]
  subnets            = [aws_subnet.flask_app_subnet_1a.id, aws_subnet.flask_app_subnet_1b.id, aws_subnet.flask_app_subnet_1c.id, ]

  enable_deletion_protection = false

  tags = {
    Name = "flask-app-alb"
  }
}

resource "aws_lb_target_group" "flask_app_alb_tg" {
  name        = "flask-app-alb-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-alb"
  }
}

resource "aws_lb_listener" "flask_app_alb_80" {
  load_balancer_arn = aws_lb.flask_app_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "flask_app_alb_443" {
  load_balancer_arn = aws_lb.flask_app_alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.domain_cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.flask_app_alb_tg.arn
  }
}

###################
## ECS Resources ##
###################

resource "aws_ecs_cluster" "flask_cluster" {
  name = "flask-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "flask_app_container_td" {
  cpu                = 256
  memory             = 512
  execution_role_arn = "arn:aws:iam::622508827640:role/ecsTaskExecutionRole"
  family             = "flask-app"
  network_mode       = "awsvpc"
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  requires_compatibilities = ["FARGATE"]
  container_definitions = jsonencode([
    {
      name  = "flask-app"
      image = "622508827640.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest"

      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "flask_app_svc" {
  name            = "flask-app-svc"
  cluster         = aws_ecs_cluster.flask_cluster.id
  desired_count   = 1
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.flask_app_container_td.arn

  depends_on = [
    aws_lb.flask_app_alb
  ]

  load_balancer {
    target_group_arn = aws_lb_target_group.flask_app_alb_tg.arn
    container_name   = "flask-app"
    container_port   = 80
  }

  network_configuration {
    assign_public_ip = "true"
    #security_groups = ""  
    subnets = [aws_subnet.flask_app_subnet_1a.id]
  }
}

###################
## KMS Resources ##
###################

resource "aws_kms_key" "flask_app_db_kms" {
  description             = "flask app db kms"
  deletion_window_in_days = 10
}

resource "aws_kms_alias" "flask_app_db_kms_alias" {
  name          = "alias/my-key-alias"
  target_key_id = aws_kms_key.flask_app_db_kms.key_id
}

########################
## Route-53 Resources ##
########################

#resource "aws_route53_record" "flask_app" {
#  zone_id = data.aws_route53_zone.bum_tv.zone_id
#  name    = "bumtelevision.com"
#  type    = "A"  

#  alias {
#    name                   = aws_lb.flask_app_alb.dns_name
#    zone_id                = aws_lb.flask_app_alb.zone_id
#    evaluate_target_health = true
#  }

#}

########################
## RDS Resources ##
########################

resource "aws_rds_cluster" "flask_app_db_cluster" {
  cluster_identifier     = "flask-app-db-cluster"
  db_subnet_group_name   = aws_db_subnet_group.flask_app_subnet_group.name
  engine                 = "aurora-mysql"
  engine_mode            = "provisioned"
  engine_version         = "8.0.mysql_aurora.3.02.0"
  database_name          = "flask_app_db"
  master_username        = "tvbum_admin"
  master_password        = "od9KN7pOhEV32oz"
  vpc_security_group_ids = [aws_security_group.flask_app_sg.id]

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster_instance" "flask_app_db" {
  cluster_identifier   = aws_rds_cluster.flask_app_db_cluster.id
  db_subnet_group_name = aws_db_subnet_group.flask_app_subnet_group.name
  identifier           = "flask-app-rds-cluster"
  instance_class       = "db.serverless"
  engine               = aws_rds_cluster.flask_app_db_cluster.engine
  engine_version       = aws_rds_cluster.flask_app_db_cluster.engine_version
  publicly_accessible  = true

}

resource "aws_db_subnet_group" "flask_app_subnet_group" {
  name       = "flask-app-subnet-group"
  subnet_ids = [aws_subnet.flask_app_subnet_1a.id, aws_subnet.flask_app_subnet_1b.id, aws_subnet.flask_app_subnet_1c.id, ]

  tags = {
    Name = "flask-app-subnet-group"
  }
}

resource "aws_db_parameter_group" "flask_app_pg" {
  name   = "rds-pg"
  family = "mysql8.0"

  parameter {
    name  = "character_set_server"
    value = "utf8"
  }

  parameter {
    name  = "character_set_client"
    value = "utf8"
  }
}

###############################
## Secrets Manager Resources ##
###############################

resource "aws_secretsmanager_secret" "flask_app_db_user" {
  name = "flask-app-db-user"
}

resource "aws_secretsmanager_secret" "flask_app_db_pass" {
  name = "flask-app-db-pass"
}

##############################
## Security Group Resources ##
##############################

resource "aws_security_group" "flask_app_sg" {
  description = "Security group for flask app rds"
  name        = "flask-app-sg"
  vpc_id      = aws_vpc.flask_app_vpc.id
}

###################
## VPC Resources ##
###################

resource "aws_vpc" "flask_app_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "flask-app-vpc"
  }
}

resource "aws_subnet" "flask_app_subnet_1a" {
  availability_zone       = "us-east-1a"
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1a"
  }
}

resource "aws_subnet" "flask_app_subnet_1b" {
  availability_zone       = "us-east-1b"
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1b"
  }
}

resource "aws_subnet" "flask_app_subnet_1c" {
  availability_zone       = "us-east-1c"
  cidr_block              = "10.0.3.0/24"
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1c"
  }
}

resource "aws_route_table" "flask_app_route_table" {
  vpc_id = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-route-table"
  }
}

resource "aws_route_table_association" "subnet_1a" {
  subnet_id      = aws_subnet.flask_app_subnet_1a.id
  route_table_id = aws_route_table.flask_app_route_table.id
}

resource "aws_route_table_association" "subnet_1b" {
  subnet_id      = aws_subnet.flask_app_subnet_1b.id
  route_table_id = aws_route_table.flask_app_route_table.id
}

resource "aws_route_table_association" "subnet_1c" {
  subnet_id      = aws_subnet.flask_app_subnet_1c.id
  route_table_id = aws_route_table.flask_app_route_table.id
}

resource "aws_internet_gateway" "flask_app_igw" {
  vpc_id = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-igw"
  }
}

resource "aws_route" "flask_app_route_igw" {
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.flask_app_igw.id
  route_table_id         = aws_route_table.flask_app_route_table.id
}
