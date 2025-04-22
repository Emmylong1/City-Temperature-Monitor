module "eks" {
source                = "../../../modules/infra"
env                   = "production"
is_eks_role_enabled             = true
is_eks_nodegroup_role_enabled   = true
cidr-block                      = "10.0.0.0/16"
vpc-name              = "vpc"
igw-name              = "igw"
pub-subnet-count      = 3
pub-cidr-block        = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
pub-availability-zone = ["us-east-1a", "us-east-1b", "us-east-1c"]
pub-sub-name          = "subnet-public"
pri-subnet-count      = 3
pri-cidr-block        = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
pri-availability-zone = ["us-east-1a", "us-east-1b", "us-east-1c"]
pri-sub-name          = "subnet-private"
public-rt-name        = "public-route-table"
private-rt-name       = "private-route-table"
eip-name              = "elasticip-ngw"
ngw-name              = "ngw"
eks-sg                = "eks-sg"

# RDS DB Configuration
db_name               = "mydb"
engine_version        = "16.3"
instance_class        = "db.t3.micro"
allocated_storage     = 20           
allowed_cidrs         = ["10.0.0.0/16"]  
environment           = "production"
# EKS
is-eks-cluster-enabled     = true
cluster-version            = "1.29"
cluster-name               = "eks-cluster"
endpoint-private-access    = true
endpoint-public-access     = true
ondemand_instance_types    = ["t2.small"]
spot_instance_types        = ["t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small", "t2.small"]
desired_capacity_on_demand = "1"
min_capacity_on_demand     = "1"
max_capacity_on_demand     = "5"
desired_capacity_spot      = "1"
min_capacity_spot          = "1"
max_capacity_spot          = "10"
ssh_key_name               = "testkey"
addons = [
  {
    name    = "vpc-cni",
    version = "v1.18.1-eksbuild.1"
  },
  {
    name    = "coredns"
    version = "v1.11.1-eksbuild.9"
  },
  {
    name    = "kube-proxy"
    version = "v1.29.3-eksbuild.2"
  },
  {
    name    = "aws-ebs-csi-driver"
    version = "v1.30.0-eksbuild.1"
  }
  # Add more addons as needed
]
}

#module "kinesis" {
 # source           = "../../modules/kinesis"
 # stream_name      = "drone-data-stream"
 # shard_count      = 2
 # retention_period = 48
#}


#module "lambda_processor" {
#  source           = "../../modules/lambda"
 # function_name    = "kinesis-processor"
  #handler          = "lambda_function.lambda_handler"
  #runtime          = "python3.10"
  #emory_size      = 512
  #timeout          = 30
  #ambda_s3_bucket = "your-lambda-bucket"
  #lambda_s3_key    = "lambda.zip"
#}

#module "database" {
 # source             = "../../modules/database"
  #allocated_storage  = 20
  #engine_version     = "16.3"
  #instance_class     = "db.t3.medium"
  #db_name            = "mydatabase"
  #username           = "dronedb"
  #password           = "mypassword"
  #subnet_ids         = module.network.private_subnet_ids
  #security_group_ids = [module.network.rds_sg_id] 
#}

#module "s3" {
 # source = "../../modules/s3"
#}

#module "ingress-controller" {
 # source     = "../../modules/ingress-controller/helm-chart-values"
 #}

#module "argocd" {
 #source     = "../../modules/argocd/helm-chart-values"
  #depends_on = [module.ingress-controller]
#}

#module "prometheus" {
 # source     = "../../modules/prometheus/helm-chart-values"
 # depends_on = [module.ingress-controller]
#}

#module "grafana" {
 # source     = "../../modules/grafana/helm-chart-values"
  #depends_on = [module.ingress-controller]
#}