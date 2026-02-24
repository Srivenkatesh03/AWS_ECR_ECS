# AWS ECS Fargate CI/CD with Jenkins, Terraform & Docker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Description

End-to-end CI/CD pipeline for deploying a Python Flask microservice to AWS ECS Fargate using Jenkins, Terraform, and Docker. Includes complete infrastructure-as-code for VPC, ECS cluster, ALB, and ECR.

## Features

- **Containerized microservice** – Python Flask app served via Docker
- **Infrastructure as Code** – Terraform provisions all AWS resources (VPC, ECS Fargate cluster, ALB, ECR, IAM)
- **Automated pipeline** – Jenkins pipeline builds, tags, pushes the image to ECR, then plans and applies Terraform
- **Smoke test** – Post-deploy stage hits the ALB endpoint to confirm the service is healthy
- **Git-SHA image tagging** – Every push produces a uniquely tagged image in ECR plus a rolling `:latest` tag

## Architecture

```
GitHub → Jenkins → Docker Build → ECR
                              ↓
                    Terraform Apply
                              ↓
          VPC (2 public subnets, 2 AZs)
                              ↓
          ALB  →  ECS Fargate Cluster  →  Flask App (:8080)
```

## Repository Structure

```
AWS_ECR_ECS/
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── terraform/
│   ├── ecr.tf
│   ├── ecs.tf
│   ├── iam.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── variables.tf
│   └── vpc.tf
├── Jenkinsfile
├── .gitignore
└── README.md
```

## Prerequisites

- AWS account with appropriate IAM permissions (ECR, ECS, VPC, ALB, IAM)
- Jenkins server with **Docker**, **Terraform**, and **AWS CLI** installed
- Jenkins credentials configured (AWS access key + secret) stored as `aws-creds`
- Terraform v1.2+
- Docker installed

## Quick Start – Local Development

```bash
# Build and test locally
cd app
docker build -t svc-demo:local .
docker run -p 8080:8080 svc-demo:local
curl http://localhost:8080
# Expected response: {"message": "Hello from ECS Fargate!", "version": "v1"}
```

## Deployment Instructions

### Jenkins Pipeline Setup

1. Create a new **Pipeline** job in Jenkins.
2. Point it at this repository (SCM → Git).
3. Under **Credentials**, add an **AWS credentials** binding with ID `aws-creds` (AWS Access Key ID + Secret Access Key).
4. Trigger a build – the pipeline will execute all stages automatically.

### Manual Terraform Deployment

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Configuration Variables

Override defaults by passing `-var` flags to Terraform:

| Variable         | Default         | Description                     |
|------------------|-----------------|---------------------------------|
| `region`         | `ap-south-1`    | AWS region                      |
| `project`        | `svc-demo`      | Project/resource name prefix    |
| `cidr`           | `10.0.0.0/16`   | VPC CIDR block                  |
| `public_subnets` | `["10.0.1.0/24","10.0.2.0/24"]` | Public subnet CIDRs |
| `desired_count`  | `2`             | Number of Fargate tasks         |
| `container_port` | `8080`          | Container listening port        |

## Infrastructure Components

| Component | Details |
|-----------|---------|
| **VPC** | Custom VPC with public subnets across 2 AZs |
| **ECS Cluster** | Fargate launch type – no EC2 instances to manage |
| **Application Load Balancer** | Routes HTTP traffic to Fargate tasks |
| **ECR** | Private Docker image repository |
| **Security Groups** | Least-privilege ingress/egress rules |
| **IAM Roles** | ECS task execution role for ECR pull and CloudWatch logs |

## Jenkins Pipeline Stages

1. **Checkout** – clone repo, capture git short SHA as `IMAGE_TAG`
2. **Build Docker Image** – `docker build` inside `app/`
3. **Authenticate & Push to ECR** – ECR login, create repo if absent, tag + push `:<sha>` and `:latest`
4. **Terraform Init & Plan** – initialize providers, produce `tfplan`
5. **Terraform Apply (deploy)** – apply the saved plan to AWS
6. **Post-deploy Smoke Test** – `curl` the ALB DNS name to confirm the service responds

## Outputs

After `terraform apply` completes the following outputs are printed:

| Output | Description |
|--------|-------------|
| `alb_dns_name` | DNS name of the Application Load Balancer |
| `ecr_repo_url` | Full URL of the ECR repository |

## Customization

Edit `terraform/variables.tf` (or pass `-var` overrides) to change the AWS region, project name, number of tasks, or subnet CIDRs without touching any other file.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `docker: permission denied` on Jenkins | Add the `jenkins` user to the `docker` group: `sudo usermod -aG docker jenkins` |
| `No credential found` Terraform error | Ensure `aws-creds` Jenkins credential ID matches the `withCredentials` block |
| ALB returns 502/503 | Check ECS task logs in CloudWatch; the task may still be starting up |
| ECR push fails with 404 | The ECR repo is created automatically by the pipeline if missing; verify IAM permissions |

## Clean Up

To avoid ongoing AWS charges, destroy all provisioned resources:

```bash
cd terraform
terraform destroy
```

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-change`.
3. Commit your changes with clear messages.
4. Open a pull request against `main`.

## License

This project is licensed under the [MIT License](LICENSE).
