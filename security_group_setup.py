import boto3

def create_emr_security_group():
    ec2 = boto3.client('ec2')
    
    # Get default VPC if not specified
    vpcs = ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
    vpc_id = vpcs['Vpcs'][0]['VpcId'] if vpcs['Vpcs'] else None
    
    if not vpc_id:
        raise Exception("No default VPC found")
    
    # Create security group with proper description
    sg = ec2.create_security_group(
        GroupName='EMR_SecurityGroup',
        Description='EMR Cluster Communication',
        VpcId=vpc_id,
        TagSpecifications=[{
            'ResourceType': 'security-group',
            'Tags': [{'Key': 'Name', 'Value': 'EMR-Cluster-SG'}]
        }]
    )
    

    # Return group ID immediately after creation
    return sg['GroupId']

if __name__ == "__main__":
    create_emr_security_group()