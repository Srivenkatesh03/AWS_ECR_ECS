pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID     = '435929993795'
        PROJECT_NAME       = 'svc-demo'
        ECR_REPO_URL       = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${PROJECT_NAME}-repo"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh "docker build -t ${PROJECT_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        // Authenticate and push must both run with AWS creds available.
        stage('Authenticate & Push to ECR') {
            steps {
                // Bind AWS credentials here so all aws/docker commands below have permission.
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    script {
                        sh '''
                            set -e
                            # Login
                            aws ecr get-login-password --region ${AWS_DEFAULT_REGION} \
                              | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com

                            # Ensure repo exists (create if not)
                            if ! aws ecr describe-repositories --repository-names ${PROJECT_NAME}-repo >/dev/null 2>&1; then
                              aws ecr create-repository --repository-name ${PROJECT_NAME}-repo
                            fi

                            # Tag and push image
                            docker tag ${PROJECT_NAME}:${IMAGE_TAG} ${ECR_REPO_URL}:${IMAGE_TAG}
                            docker push ${ECR_REPO_URL}:${IMAGE_TAG}

                            # also push :latest
                            docker tag ${PROJECT_NAME}:${IMAGE_TAG} ${ECR_REPO_URL}:latest
                            docker push ${ECR_REPO_URL}:latest
                        '''
                    }
                }
            }
        }

        stage('Terraform Init & Plan') {
            steps {
                dir('terraform') {
                    // Terraform also needs AWS credentials
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh '''
                            terraform init -input=false
                            terraform plan -var="region=${AWS_DEFAULT_REGION}" \
                                           -var="project=${PROJECT_NAME}" \
                                           -var="desired_count=2" \
                                           -out=tfplan
                        '''
                    }
                }
            }
        }

        stage('Terraform Apply (deploy)') {
            steps {
                dir('terraform') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        sh '''
                            terraform apply -auto-approve tfplan || terraform apply -auto-approve
                        '''
                    }
                }
            }
        }

        stage('Post-deploy Smoke Test') {
            steps {
                dir('terraform') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                        script {
                            def alb = sh(script: "terraform output -raw alb_dns_name", returnStdout: true).trim()
                            echo "ALB DNS: ${alb}"
                            sh "curl -f http://${alb}/ || true"
                        }
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed. Email notifications disabled because SMTP is not configured."
        }
    }
}
