# City-Temperature-Monitor

## Overview
This project designs, implements, and maintains a robust, scalable, and containerized infrastructure for collecting and storing temperature data from multiple cities. It ensures high availability, reliability, and efficient data management.

## Architecture Diagram
![image alt](https://github.com/Emmylong1/Drone-Data/blob/29b7ead546a629ad45b4830091956baeaf86db67/image.png)

## Setup Instructions
1. [Clone the repository](https://github.com/Emmylong1/Drone-Data/tree/emmydev).
2. Navigate to the `drone-data-ingestion` directory.
3. Run `deploy.py` to provision the entire infrastructure in one step, without manually running `terraform init` or `terraform apply`.

## Components
- **Terraform**: Manages cloud infrastructure.
- **Networking**: NGINX Ingress for traffic management, VPC peering for security.
- **Docker**: Containerizes applications.
- **Compute**: Kubernetes cluster (EKS) to manage microservices.
- **Streaming Data**: AWS Kinesis for real-time data ingestions and processing.
- **Processing**: AWS Lambda Functions for real-time data processing
- **Storage**: S3/Storage for raw drone data, PostgreSQL for structured metadata.
- **Auto-Scaling**: Kubernetes HPA (Horizontal Pod Autoscaler) based on CPU/memory utilization.
- **Monitoring**: Tracks system health.

## CI/CD Pipeline Setup

- **CI/CD Workflow**:

- **Version Control**: GitHub for source code management.

- **CI/CD Tool**: ArgoCD for GitOps-driven continuous delivery.

- **Build & Test**: Terraform for infrastructure as code, Helm for Kubernetes deployments.

- **Automation**: GitHub Actions for pipeline automation.

## Steps:

Push code to repository.

CI/CD pipeline triggers Terraform for infrastructure setup.

Docker builds and pushes container images to a registry.

ArgoCD applies Kubernetes manifests and Helm charts.

Kubernetes deploys updated microservices.

## Monitoring & Logging

### Proposed Monitoring & Logging Stack:

- **Metrics**: Prometheus & Grafana for performance monitoring.

- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana) for log aggregation.

- **Alerting**: Prometheus Alertmanager or PagerDuty for notifications.

## Future Enhancements
- Implement CI/CD pipeline.
- Add automated IPFS storage.

## Troubleshooting
- Check the logs in grafana for Eks service issues.
- Verify the IPFS daemon is running for data storage.



