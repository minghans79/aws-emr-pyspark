from iam_setup import create_emr_roles
from s3_setup import create_s3_buckets, upload_emr_files
from security_group_setup import create_emr_security_group
from emr_setup import create_emr_cluster
from ec2 import create_key_pair
import boto3
import argparse

def deploy_infra():
    print("Creating IAM Roles...")
    create_emr_roles()
    
    print("\nCreating S3 Buckets...")
    create_s3_buckets()

    print("\nUploading EMR Files...")
    upload_emr_files()
    
    print("\nCreating Security Group...")
    sg_id = create_emr_security_group()
    
    print("\nCreating EC2 Key Pair...")
    create_key_pair('Default_Key')

    print("\nCreating EMR Cluster...")
    cluster_id = create_emr_cluster(sg_id,'Default_Key')
    
    print(f"\nEMR Cluster ID: {cluster_id}")

if __name__ == "__main__":
    deploy_infra()