from emr_cleanup import terminate_emr_cluster
from security_group_cleanup import delete_emr_security_group
from s3_cleanup import delete_s3_buckets
from iam_cleanup import delete_iam_resources
from ec2 import delete_key_pair
import time
import argparse
import os

def cleanup_infra():
    # print("Terminating EMR Cluster...")
    # #terminate_emr_cluster()
    # #os.remove('Default_Key.pem')
    
    # # Wait for cluster termination to complete
    # print("\nWaiting 2 minutes for resources to release...")
    # time.sleep(120)

    print("\nDeleting Key Pair...")
    delete_key_pair('Deafult_Key')
    
    print("\nDeleting Security Group...")
    delete_emr_security_group()
    
    print("\nDeleting S3 Buckets...")
    delete_s3_buckets()
    
    print("\nCleaning IAM Resources...")
    delete_iam_resources()
    
    print("\nCleanup complete!")

if __name__ == "__main__":      
    cleanup_infra()