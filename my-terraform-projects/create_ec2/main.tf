provider "aws" {
  region = "us-east-1" 
}

data "aws_ami" "amazon_linux_2023" {
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }

  owners = ["137112412989"] # Amazon official AMI owner
}

resource "aws_instance" "amazon_linux_instance" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = "t2.micro" 
  key_name               = "my-lab-key" 
  vpc_security_group_ids = ["sg-066db9076a06b7585"] 

  tags = {
    Name = "AmazonLinux2023-Instance"
  }
}
