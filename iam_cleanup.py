import boto3

def delete_iam_resources():
    iam = boto3.client('iam')
    
    # Delete EC2 Instance Profile
    try:
        iam.remove_role_from_instance_profile(
            InstanceProfileName='EMR_EC2_DefaultRole',
            RoleName='EMR_EC2_DefaultRole'
        )
        iam.delete_instance_profile(
            InstanceProfileName='EMR_EC2_DefaultRole'
        )
        print("Deleted EC2 instance profile")
    except iam.exceptions.NoSuchEntityException:
        pass
    
    # Delete Roles
    roles = ['EMR_DefaultRole', 'EMR_EC2_DefaultRole']
    
    for role in roles:
        try:
            # Detach policies
            policies = iam.list_attached_role_policies(RoleName=role)['AttachedPolicies']
            for policy in policies:
                iam.detach_role_policy(
                    RoleName=role,
                    PolicyArn=policy['PolicyArn']
                )

            inline_policies = iam.list_role_policies(RoleName=role)['PolicyNames']
            for policy_name in inline_policies:
                iam.delete_role_policy(
                RoleName=role,
                PolicyName=policy_name
            )

            # Delete role
            iam.delete_role(RoleName=role)
            print(f"Deleted role: {role}")
            
        except iam.exceptions.NoSuchEntityException:
            print(f"Role {role} does not exist")


if __name__ == "__main__":
    delete_iam_resources()