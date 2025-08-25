import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

s3_client = boto3.client(
    "s3",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = AWS_REGION
)

def upload_file(local_filepath, s3_filepath):
    try:
        s3_client.upload_file(local_filepath, S3_BUCKET, s3_filepath)
        print(f"Uploaded {local_filepath} to s3 with filepath of {s3_filepath}")
    except Exception as e:
        print(f"Error in uploading {local_filepath}")

if __name__ == "__main__":
    local_files = {
        "data/raw/olist_customers_dataset.csv": "raw/customers/olist_customers_dataset.csv",
        "data/raw/olist_orders_dataset.csv": "raw/orders/olist_orders_dataset.csv",
    }

    for local_path, s3_filepath in local_files.items():
        if os.path.exists(local_path):
            upload_file(local_path, s3_filepath)
        else:
            print(f"file not found: {local_path}")