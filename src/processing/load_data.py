import os
import boto3
import pandas as pd
import io
from dotenv import load_dotenv

load_dotenv()
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

s3_client = boto3.client("s3", region_name=AWS_REGION)

CUSTOMERS_KEY = "raw/customers/olist_customers_dataset.csv"
ORDERS_KEY = "raw/orders/olist_orders_dataset.csv"

def load_csv(bucket: str, key: str) -> pd.DataFrame:
    response = s3_client.get_object(Bucket=bucket, Key=key)
    csv_data = response["Body"].read().decode("utf-8")
    return pd.read_csv(io.StringIO(csv_data))

def load_customers() -> pd.DataFrame:
    return load_csv(S3_BUCKET, CUSTOMERS_KEY)

def load_orders() -> pd.DataFrame:
    return load_csv(S3_BUCKET, ORDERS_KEY)
