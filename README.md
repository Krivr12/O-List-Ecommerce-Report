# AWS E-Commerce Data Analysis

This project analyzes the **Olist E-Commerce dataset** using **AWS Athena**, **Amazon S3**, and **Python** (PyAthena & Pandas).  
The goal is to clean, transform, and analyze customer and order data, then generate useful KPIs for insights.

---

## Features

- Load and clean raw Olist datasets.
- Query datasets using **AWS Athena** with SQL.
- Filter orders (e.g., by date range `2017-01-01` → `2018-09-01`).
- Save **processed CSVs** for analysis.
- Upload both raw and processed datasets to **Amazon S3**.
- Jupyter notebooks for:
  - **Business Performance** (revenue, orders, customer growth).
  - **Operational Analysis** (delivery performance, order status).
- Dashboard app for visualization.

---

## Requirements

- Python 3.8+
- AWS Account with **S3** & **Athena** enabled
- Python packages (install via `requirements.txt`):

```bash
pip install -r requirements.txt
```

## Usage
1. Prepare Data
Upload raw datasets (olist_customers_dataset.csv, olist_orders_dataset.csv) into data/raw/.
2. Upload to S3
```bash
python src/aws/s3_upload.py
```
3. Run Athena Queries
```bash
python src/aws/athena_query.py
```
4. Process Data
Clean and filter datasets locally:4. 
```bash
python src/processing/cleaning_data.py
python src/processing/filtering_data.py
```
5. Upload Processed Data
```bash
python src/aws/s3_upload_processed_data.py
```
6. Explore Insights

- Open Jupyter notebooks under notebook/.

- Run dashboard/dashboard.py for visualization.


Developed by Chris Evangelista
Polytechnic University of the Philippines | AWS Cloud Clubs PUP
