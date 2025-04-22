# City-Temperature-Monitor

## Overview
This project designs, implements, and maintains a robust, scalable, and containerized infrastructure for collecting and storing temperature data from multiple cities. It ensures high availability, reliability, and efficient data management.

### System Architecture

![Temperature Data Collection System Architecture](https://raw.githubusercontent.com/Emmylong1/City-Temperature-Monitor/main/temperature-architecture.svg)

## Components
The architecture consists of the following components:
- **Terraform**: Manages cloud infrastructure.
- **Networking**: NGINX Ingress for traffic management.
- **Docker**: Containerizes applications.
- **Compute**: Kubernetes cluster (EKS) to manage microservices.
- **Streaming Data**: AWS Kinesis for real-time data ingestions and processing.
- **Storage**: S3/Storage for raw drone data, PostgreSQL for structured metadata.
- **Data Collection**: Temperature scraper that collects data from wttr.in API
- **Message Broker**: Kafka for reliable message passing
- **Storage**: Relational database and IPFS for data storage
- **Cloud Infrastructure**: Kubernetes with auto-scaling and ArgoCD for GitOps
- **Monitoring & Logging**: Prometheus and Grafana for system observability
- **CI/CD Pipeline**: GitHub, CI/CD automation, and DockerHub for container registry