import boto3

def delete_emr_security_group():
    ec2 = boto3.client('ec2')
    
    try:
        sgs = ec2.describe_security_groups(
            GroupNames=['EMR_SecurityGroup']
        )['SecurityGroups']
        
        if sgs:
            ec2.delete_security_group(GroupId=sgs[0]['GroupId'])
            print(f"Deleted security group: {sgs[0]['GroupId']}")
            
    except ec2.exceptions.ClientError as e:
        if 'does not exist' in str(e):
            print("Security group already deleted")
        else:
            raise

if __name__ == "__main__":
    delete_emr_security_group()