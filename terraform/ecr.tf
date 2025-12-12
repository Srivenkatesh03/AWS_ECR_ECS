# terraform/ecr.tf
resource "aws_ecr_repository" "app" {
  name = "${var.project}-repo"
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = { Name = "${var.project}-ecr" }
}
