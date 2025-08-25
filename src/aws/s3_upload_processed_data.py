import boto3
import os
from dotenv import load_dotenv

# Load AWS creds
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Local processed files → S3 paths
processed_files = {
    "data/processed/customers_processed.csv": "processed/customers/customers_processed.csv",
    "data/processed/orders_processed.csv": "processed/orders/orders_processed.csv",
}

# Upload each file
for local_path, s3_key in processed_files.items():
    if os.path.exists(local_path):
        try:
            s3_client.upload_file(local_path, S3_BUCKET, s3_key)
            print(f"✅ Uploaded {local_path} → s3://{S3_BUCKET}/{s3_key}")
        except Exception as e:
            print(f"❌ Failed to upload {local_path}: {e}")
    else:
        print(f"⚠️ File not found: {local_path}")
