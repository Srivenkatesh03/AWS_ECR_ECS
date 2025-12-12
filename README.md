# AWS ECS Fargate CI/CD with Jenkins, Terraform & Docker

## Overview
This project demonstrates an end-to-end CI/CD pipeline for a Python microservice:
- Containerize app (Docker)
- Push images to ECR
- Provision infra (VPC, ECS Cluster, ALB, ECR) using Terraform
- Jenkins pipeline builds image, pushes to ECR, and runs Terraform to deploy to ECS (Fargate)

## Repo layout
See repository layout in README (top level).

## Prerequisites
- AWS account
- Jenkins server or agent with Docker, Terraform, AWS CLI installed
- Jenkins credentials (AWS access key + secret) stored in Jenkins as `aws-creds`
- Terraform v1.2+
- Docker installed on builder machine

## Quick start (local / test)
1. Build & test locally:
   ```bash
   cd app
   docker build -t svc-demo:local .
   docker run -p 8080:8080 svc-demo:local
   curl http://localhost:8080
