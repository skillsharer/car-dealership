import boto3
import os

def handler(event, context):
    s3_client = boto3.client('s3')
    bucket_path = os.getenv('LANDING_ZONE')
    print(f'Bucket path: {bucket_path}')
    

if __name__ == '__main__':
    handler("", "")