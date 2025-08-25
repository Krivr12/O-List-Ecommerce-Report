import pandas as pd
from load_data import load_customers, load_orders

def clean_orders():
    orders_df = load_orders()


    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for column in date_columns:
        orders_df[column] = pd.to_datetime(orders_df[column], errors="coerce")

    # Rename columns
    orders_df.rename(
        columns={
            "order_purchase_timestamp": "order_purchase_dt",
            "order_approved_at": "order_approved_dt",
            "order_delivered_carrier_date": "order_delivered_carrier_dt",
            "order_delivered_customer_date": "order_delivered_customer_dt",
            "order_estimated_delivery_date": "order_estimated_delivery_dt"
        },
        inplace=True
    )

    # Convert status to categorical
    orders_df["order_status"] = orders_df["order_status"].astype("category")

    return orders_df


def clean_customers():
    customers_df = load_customers()

    # Normalize strings
    customers_df["customer_city"] = customers_df["customer_city"].str.strip().str.title()
    customers_df["customer_state"] = customers_df["customer_state"].str.strip().str.upper()

    # Convert to categorical
    customers_df[["customer_city", "customer_state"]] = (
        customers_df[["customer_city", "customer_state"]].astype("category")
    )

    return customers_df
