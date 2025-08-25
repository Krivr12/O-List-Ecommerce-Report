import os
import boto3
from dotenv import load_dotenv
import time

load_dotenv()
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET") 
S3_OUTPUT = f"s3://{S3_BUCKET}/athena-results/"

athena_client = boto3.client("athena", region_name=AWS_REGION)
s3_client = boto3.client("s3")

def athena_query(query, database=None):
    params = {
        "QueryString": query,
        "ResultConfiguration": {"OutputLocation": S3_OUTPUT},
    }
    if database:
        params["QueryExecutionContext"] = {"Database": database}

    response = athena_client.start_query_execution(**params)
    query_execution_id = response["QueryExecutionId"]

    # wait until finished
    while True:
        status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(2)

    if state != "SUCCEEDED":
        return []

    # only SELECT queries return rows
    if not query.strip().lower().startswith("select"):
        return []

    result = athena_client.get_query_results(QueryExecutionId=query_execution_id)
    rows = result["ResultSet"]["Rows"]

    if len(rows) > 1:
        headers = [col.get("VarCharValue", "") for col in rows[0]["Data"]]
        data = []
        for row in rows[1:]:
            values = [col.get("VarCharValue", "") for col in row["Data"]]
            data.append(dict(zip(headers, values)))
        return data
    else:
        return []




print("\nChecking S3 files under raw/customers/ and raw/orders/ ...\n")

def list_s3_files(prefix):
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
    if "Contents" in response:
        for obj in response["Contents"]:
            print(obj["Key"])

list_s3_files("raw/customers/")
list_s3_files("raw/orders/")




create_db = "CREATE DATABASE IF NOT EXISTS olist_ecommerce_db"
athena_query(create_db)

create_customers = f"""
CREATE EXTERNAL TABLE IF NOT EXISTS customers (
    customer_id STRING,
    customer_unique_id STRING,
    customer_zip_code_prefix INT,
    customer_city STRING,
    customer_state STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
LOCATION 's3://{S3_BUCKET}/raw/customers/'
TBLPROPERTIES ('skip.header.line.count'='1');
"""
athena_query(create_customers, database="olist_ecommerce_db")

create_orders = f""" 
CREATE EXTERNAL TABLE IF NOT EXISTS orders (
    order_id STRING,
    customer_id STRING,
    order_status STRING,
    order_purchase_timestamp STRING,
    order_approved_at STRING,
    order_delivered_carrier_date STRING,
    order_delivered_customer_date STRING,
    order_estimated_delivery_date STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
LOCATION 's3://{S3_BUCKET}/raw/orders/'
TBLPROPERTIES ('skip.header.line.count'='1');
"""
athena_query(create_orders, database="olist_ecommerce_db")




print("\nRunning KPI Queries...\n")

kpis = {}

Total_Customers = """
SELECT COUNT(DISTINCT customer_unique_id) AS total_customers FROM customers;
"""
kpis.update(athena_query(Total_Customers, database="olist_ecommerce_db")[0])

Total_Orders = """
SELECT COUNT(DISTINCT order_id) AS total_orders FROM orders;
"""
kpis.update(athena_query(Total_Orders, database="olist_ecommerce_db")[0])

Delivered_Orders = """
SELECT COUNT(DISTINCT order_id) AS delivered_orders 
FROM orders WHERE order_status = 'delivered';
"""
kpis.update(athena_query(Delivered_Orders, database="olist_ecommerce_db")[0])

print("\n--- KPI Summary ---")
for k, v in kpis.items():
    print(f"{k}: {v}")




print("\nChecking for duplicates...\n")

Duplicate_Customers = """
SELECT COUNT(*) AS duplicate_customers
FROM (
    SELECT customer_unique_id, COUNT(*) AS c
    FROM customers
    GROUP BY customer_unique_id
    HAVING COUNT(*) > 1
);
"""
print(athena_query(Duplicate_Customers, database="olist_ecommerce_db")[0])

Duplicate_Orders = """
SELECT COUNT(*) AS duplicate_orders
FROM (
    SELECT order_id, COUNT(*) AS c
    FROM orders
    GROUP BY order_id
    HAVING COUNT(*) > 1
);
"""
print(athena_query(Duplicate_Orders, database="olist_ecommerce_db")[0])
