# Business and Operation Analysis for Brazilian E-Commerce 
## Executive Summary:

Using Python and AWS, I pulled the data from the cloud storage and created a dashboard to easily track our progress. I identified that the largest bottleneck in our operation is "Carrier -> Customer" Stage and that customer retention rate is low, with 3.9% being the highest. With that, the largest revenue opportunities are to increase and identify strategic warehouse location and to create actions like loyalty discounts and repeat order promos. I recommend that the logistic and marketing team create a joint operation they will review the process and suggest changes that would lead to:

1. Faster delivery rate, especially on low performing regions like Bahia.
2. Higher customer retention rate.
3. Maintain the momentum and further grow demand in emerging states like Parana.
4. Drastic increase in revenue.

---
## Business Problem:

Fast and on-time orders are essential for an e-commerce platform like Olist, this affect customer satisfaction and retention rate. I noticed that there's a severe delayed delivery in order states, with some reaching up to 26 days, almost doubled the average delivery times of 12 days, and aside from that it is also visible that we still have a low retention rate. The goal is how can we identify on which stage in the operation might be the root cause of this delayed 

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
