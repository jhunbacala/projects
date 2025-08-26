
// Collect the latest ami for Amazon Linux
data "aws_ami" "latest_ami" {
  most_recent = "true"
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}


// Security Groups for SSH Access
resource "aws_security_group" "allow_ssh" {
  name_prefix = "allow_ssh"
  description = "Allow SSH access for EC2 Instance Connect"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

// IAM Role for EC2 Instace Connect
resource "aws_iam_role" "ec2_instance_connect" {
  name               = "EC2InstanceConnectRole"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF  
}

// Attach EC2 Instance Connect IAM Policy
resource "aws_iam_policy_attachment" "ec2_connect_attach" {
  name       = "ec2-connect-policy-attachment"
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  roles      = [aws_iam_role.ec2_instance_connect.name]
}

// Create IAM Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_instance_connect.name
}

// Create EC2 Instance
resource "aws_instance" "myec2" {
  ami                  = data.aws_ami.latest_ami.id
  instance_type        = "t2.micro"
  security_groups      = [aws_security_group.allow_ssh.name]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  tags = {
    Name = "Linux Instance 1"
    Env  = "Dev"
  }
}