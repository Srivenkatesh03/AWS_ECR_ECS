# terraform/variables.tf
variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "project" {
  type    = string
  default = "svc-demo"
}

variable "cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "public_subnets" {
  type    = list(string)
  default = ["10.0.1.0/24","10.0.2.0/24"]
}

variable "desired_count" {
  type    = number
  default = 2
}

variable "container_port" {
  type    = number
  default = 8080
}
