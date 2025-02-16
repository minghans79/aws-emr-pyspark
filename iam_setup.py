import boto3
import json

def create_emr_roles():
    iam = boto3.client('iam')
    
    ec2_sg_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                    "ec2:AuthorizeSecurityGroupIngress",
                    "ec2:AuthorizeSecurityGroupEgress",
                    "ec2:CancelSpotInstanceRequests",
                    "ec2:CreateNetworkInterface",
                    "ec2:CreateSecurityGroup",
                    "ec2:CreateTags",
                    "ec2:DeleteNetworkInterface",
                    "ec2:DeleteSecurityGroup",
                    "ec2:DeleteTags",
                    "ec2:DescribeAvailabilityZones",
                    "ec2:DescribeAccountAttributes",
                    "ec2:DescribeDhcpOptions",
                    "ec2:DescribeImages",
                    "ec2:DescribeInstanceStatus",
                    "ec2:DescribeInstances",
                    "ec2:DescribeKeyPairs",
                    "ec2:DescribeNetworkAcls",
                    "ec2:DescribeNetworkInterfaces",
                    "ec2:DescribePrefixLists",
                    "ec2:DescribeRouteTables",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeSpotInstanceRequests",
                    "ec2:DescribeSpotPriceHistory",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeTags",
                    "ec2:DescribeVpcAttribute",
                    "ec2:DescribeVpcEndpoints",
                    "ec2:DescribeVpcEndpointServices",
                    "ec2:DescribeVpcs",
                    "ec2:DetachNetworkInterface",
                    "ec2:ModifyImageAttribute",
                    "ec2:ModifyInstanceAttribute",
                    "ec2:RequestSpotInstances",
                    "ec2:RevokeSecurityGroupEgress",
                    "ec2:RunInstances",
                    "ec2:TerminateInstances"
            ],
            "Resource": "*"
        }
    ]
}

    # EMR Service Role
    emr_service_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "elasticmapreduce.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    emr_service_role = iam.create_role(
        RoleName='EMR_DefaultRole',
        AssumeRolePolicyDocument=json.dumps(emr_service_policy)
    )

    iam.put_role_policy(
        RoleName = 'EMR_DefaultRole',
        PolicyName='EMRSecurityGroupManagement',
        PolicyDocument=json.dumps(ec2_sg_policy)
    )
      
    iam.attach_role_policy(
        RoleName='EMR_DefaultRole',
        PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEMRServicePolicy_v2'
    )

    # EC2 Instance Profile
    ec2_trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    ec2_instance_profile = iam.create_role(
        RoleName='EMR_EC2_DefaultRole',
        AssumeRolePolicyDocument=json.dumps(ec2_trust_policy)
    )
    
    iam.attach_role_policy(  # Keep S3 access if needed
        RoleName='EMR_EC2_DefaultRole',
        PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
    )

    iam.attach_role_policy(
        RoleName='EMR_EC2_DefaultRole',
        PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role'
    )

    iam.create_instance_profile(
        InstanceProfileName='EMR_EC2_DefaultRole'
    )
    
    iam.add_role_to_instance_profile(
        InstanceProfileName='EMR_EC2_DefaultRole',
        RoleName='EMR_EC2_DefaultRole'
    )

if __name__ == "__main__":
    create_emr_roles()