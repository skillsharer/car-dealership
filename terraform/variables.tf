variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "project_name" {
  type    = string
  default = "car-dealership"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "lambda_timeout" {
  type    = number
  default = 120
}

variable "lambda_memory_size" {
  type    = number
  default = 1024
}