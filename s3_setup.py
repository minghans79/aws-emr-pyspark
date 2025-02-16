import boto3

def create_s3_buckets():
    s3 = boto3.client('s3')
    region = boto3.session.Session().region_name
    account_id = boto3.client('sts').get_caller_identity()['Account']
    
    buckets = [
        f'emr-scripts-{account_id}-{region}',
        f'emr-input-{account_id}-{region}',
        f'emr-output-{account_id}-{region}',
        f'emr-logs-{account_id}-{region}'
    ]
    
    for bucket in buckets:
        try:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                } if region != 'us-east-1' else {}
            )
            print(f"Created bucket: {bucket}")
        except s3.exceptions.BucketAlreadyExists:
            print(f"Bucket {bucket} already exists")

def upload_emr_files():
    s3 = boto3.client('s3')
    region = boto3.session.Session().region_name
    account_id = boto3.client('sts').get_caller_identity()['Account']
    
    # Get bucket names (matches creation pattern)
    script_bucket = f'emr-scripts-{account_id}-{region}'
    input_bucket = f'emr-input-{account_id}-{region}'
    
    # Upload Spark job script
    try:
        s3.upload_file(
            'script.py',
            script_bucket,
            'script.py',
            ExtraArgs={'ContentType': 'text/x-python-script'}
        )
        print(f"Uploaded script.py to s3://{script_bucket}/")
    except FileNotFoundError:
        print("Error: script.py not found in local directory")
    except Exception as e:
        print(f"Error uploading script.py: {str(e)}")

    # Upload sample input file
    try:
        s3.upload_file(
            'meta_Kindle_Store.jsonl.7z',
            input_bucket,
            'meta_Kindle_Store.jsonl.7z',
            ExtraArgs={'ContentType': 'application/x-7z-compressed'}
        )
        print(f"Uploaded meta_Kindle_Store.jsonl.7z to s3://{input_bucket}/")
    except FileNotFoundError:
        print("Error: meta_Kindle_Store.jsonl.7z not found in local directory")
    except Exception as e:
        print(f"Error uploading meta_Kindle_Store.jsonl.7z: {str(e)}")

if __name__ == "__main__":
    create_s3_buckets()
    upload_emr_files()