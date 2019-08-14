# coding: utf-8
import boto3
ec2 = boto3.resource('ec2')
ec2
key_name = "auto_aws_key"
key_path = key_name + ".pem"
key_pair = ec2.create_key_pair(KeyName=key_name)
key_pair.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key_pair.key_material)

get_ipython().run_line_magic('ls', '-l auto_aws_key.pem')
import os, stat
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
get_ipython().run_line_magic('ls', '-l auto_aws_key.pem')
ec2.images.filter(Owners=['amazon'])
list(ec2.images.filter(Owners=['amazon']))
len(list(ec2.images.filter(Owners=['amazon'])))
img = ec2.Image('ami-0b898040803850657')
img.name
ami_name = 'amzn2-ami-hvm-2.0.20190618-x86_64-gp2'
filters = [{'Name': 'name', 'Values': [ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=filters))
instance = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1,InstanceType='t2.micro', KeyName=key_pair.key_name)
instance
inst = instance[0]
inst.terminate()
instance = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1,InstanceType='t2.micro', KeyName=key_pair.key_name)
inst = instance[0]
inst.public_dns_name
inst.wait_until_exists()
inst.public_dns_name
inst.reload()
inst.public_dns_name
inst.security_groups
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(IpPermissions=[{'FromPort': 22, 'ToPort': 22, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '182.65.66.21/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort': 80, 'ToPort': 80, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])

#ASG Configuration and usage
session = boto3.Session(profile_name='samcoder')
as_client = session.client('autoscaling')
as_client
as_client.describe_auto_scaling_groups()
as_client.describe_policies()
as_client.execute_policy(AutoScalingGroupName='NotifyExample', PolicyName='ScaleUp')
as_client.execute_policy(AutoScalingGroupName='NotifyExample', PolicyName='ScaleDown')

import boto3
session = boto3.Session(profile_name='samcoder')
as_client = session.client('autoscaling')
as_client.execute_policy(AutoScalingGroupName='NotifyExample', PolicyName='ScaleUp')
