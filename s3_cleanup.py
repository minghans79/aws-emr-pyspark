import boto3

def delete_s3_buckets():
    s3 = boto3.client('s3')
    resource = boto3.resource('s3')
    account_id = boto3.client('sts').get_caller_identity()['Account']
    region = boto3.session.Session().region_name
    
    buckets = [
        f'emr-scripts-{account_id}-{region}',
        f'emr-input-{account_id}-{region}',
        f'emr-output-{account_id}-{region}',
        f'emr-logs-{account_id}-{region}'
    ]
    
    for bucket in buckets:
        try:
            # Delete all objects and versions
            bucket_resource = resource.Bucket(bucket)
            bucket_resource.object_versions.delete()
            
            # Delete bucket
            s3.delete_bucket(Bucket=bucket)
            print(f"Deleted bucket: {bucket}")
            
        except s3.exceptions.NoSuchBucket:
            print(f"Bucket {bucket} does not exist")
        except s3.exceptions.ClientError as e:
            if 'AccessDenied' in str(e):
                print(f"Warning: Could not delete {bucket} - permissions issue")
            else:
                raise

if __name__ == "__main__":
    delete_s3_buckets()