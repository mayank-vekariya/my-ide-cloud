import pulumi
import pulumi_aws as aws
from pulumi_command import remote

# Create a new security group that allows SSH and HTTP traffic
security_group = aws.ec2.SecurityGroup("allow-ssh-http",
    description="Allow SSH and HTTP traffic",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=8080,
            to_port=8080,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
)

# Create a new EC2 instance
instance = aws.ec2.Instance("code-server-instance",
    instance_type="t2.micro",
    security_groups=[security_group.name],
    ami="ami-0c55b159cbfafe1f0",  # Update with the correct AMI ID for your region
    key_name="ide2-project",  # Update with the name of your key pair
)

# Define a remote command to install and start code-server on the EC2 instance
install_code_server = remote.Command(
    "installCodeServer",
    connection=remote.ConnectionArgs(
        host=instance.public_ip,
        user="ubuntu",
        private_key="ide2-project.pem",  # Update with the correct path to your PEM key file
    ),
    create="curl -fsSL https://code-server.dev/install.sh | sh && code-server --bind-addr 0.0.0.0:8080 --auth none &",
)

# Export the public IP of the instance to access the code server
pulumi.export("3.90.68.157", instance.public_ip)
