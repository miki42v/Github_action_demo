variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "dev"
}

variable "app_name" {
  description = "App prefix"
  type        = string
  default     = "demo"
}

variable "admin_cidr" {
  description = "CIDR allowed for SSH (use your public IP, e.g. 1.2.3.4/32)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "ec2_instance_type" {
  description = "Use free-tier eligible EC2 instance type"
  type        = string
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro"], var.ec2_instance_type)
    error_message = "ec2_instance_type must be t2.micro or t3.micro for free-tier-focused setup."
  }
}

variable "enable_rds" {
  description = "Enable RDS (can still incur charges outside free-tier eligibility)."
  type        = bool
  default     = false
}

variable "rds_instance_class" {
  description = "RDS class when enable_rds=true"
  type        = string
  default     = "db.t3.micro"

  validation {
    condition     = contains(["db.t2.micro", "db.t3.micro", "db.t4g.micro"], var.rds_instance_class)
    error_message = "Use a micro class for free-tier-focused setup."
  }
}
