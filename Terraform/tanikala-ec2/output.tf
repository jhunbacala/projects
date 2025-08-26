output "latest_ami_id" {
  value = data.aws_ami.latest_ami.id
}

output "instance_id" {
  value = {
    instance_id = aws_instance.myec2.id
    public_ip   = aws_instance.myec2.public_ip
  }  
}