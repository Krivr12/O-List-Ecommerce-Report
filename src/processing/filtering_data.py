import os
import pandas as pd
import frameon as fron
from cleaning_data import clean_orders, clean_customers

def prepare_customers_orders():
    customers_df = clean_customers()
    orders_df = clean_orders()

    # Orders before January 2017 were very few (3 months have less than 2 orders) so we conclude that the data is incomplete. So We'll start at January 2017
    orders_before_march_2017 = orders_df[orders_df.order_approved_dt < '2017-04-01'].groupby(
        pd.Grouper(key='order_approved_dt', freq='ME')
    ).agg({'order_id': 'nunique'})
    print(orders_before_march_2017)

    # All orders after August 2018 we're cancelled and only one got shipperd
    orders_after_August_2018 = orders_df[orders_df.order_purchase_dt > '2018-09-01']
    print(orders_after_August_2018)

    # So we will trim the data and only get order between January 1, 2017 and September 1, 2018
    orders_df = orders_df[
        orders_df.order_purchase_dt.between(
            pd.to_datetime('2017-01-01'),
            pd.to_datetime('2018-09-01'),
            inclusive='left'
        ) | orders_df.order_purchase_dt.isna()
    ]

    # We also need to filter out the customers because we only need the ones connected to our orders list.
    customersdf_before = fron.analyze_join_keys(customers_df, orders_df, on="customer_id", how="inner")
    print(f"before: {customersdf_before}")

    customers_df = customers_df.merge(
        orders_df[["customer_id"]],
        on="customer_id",
        how="inner"
    )

    customersdf_after = fron.analyze_join_keys(customers_df, orders_df, on="customer_id", only_coverage=True)
    print(f"after: {customersdf_after}")

    customers_df.to_csv("data/processed/customers_processed.csv", index=False)
    orders_df.to_csv("data/processed/orders_processed.csv", index=False)
    print("Processed data saved in data/processed/")
    return customers_df, orders_df


if __name__ == "__main__":
    prepare_customers_orders()
