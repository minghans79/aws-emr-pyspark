import boto3
import os

ec2_client = boto3.client('ec2')

def create_key_pair(key_name):
    """
    Creates an EC2 key pair and saves the private key to a file.
    """
    try:
        # Create the key pair
        response = ec2_client.create_key_pair(KeyName=key_name)

        # Extract the private key material
        private_key = response['KeyMaterial']

        # Save the private key to a .pem file
        key_file_path = f'{key_name}.pem'
        with open(key_file_path, 'w') as key_file:
            key_file.write(private_key)

        # Set correct permissions for the private key file
        os.chmod(key_file_path, 0o400)

        print(f"Key pair '{key_name}' created successfully.")
        print(f"Private key saved to '{key_file_path}'.")
    except ec2_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
            print(f"Key pair '{key_name}' already exists.")
        else:
            print(f"An error occurred: {e}")

def delete_key_pair(key_name):
    """
    Deletes an EC2 key pair.
    """
    try:
        # Delete the key pair
        ec2_client.delete_key_pair(KeyName=key_name)
        print(f"Key pair '{key_name}' deleted successfully.")
    except ec2_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
            print(f"Key pair '{key_name}' does not exist.")
        else:
            print(f"An error occurred: {e}")