import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time,
        delay_vs_expected, order_status]
        """

        orders = self.data["orders"].copy()

        if is_delivered:
            orders = orders[
                orders["order_status"] == "delivered"
            ].copy()

        date_columns = [
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]

        for column in date_columns:
            orders[column] = pd.to_datetime(orders[column])

        orders["wait_time"] = (
            orders["order_delivered_customer_date"]
            - orders["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400

        orders["expected_wait_time"] = (
            orders["order_estimated_delivery_date"]
            - orders["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400

        orders["delay_vs_expected"] = (
            orders["order_delivered_customer_date"]
            - orders["order_estimated_delivery_date"]
        ).dt.total_seconds().div(86400).clip(lower=0)

        return orders[
            [
                "order_id",
                "wait_time",
                "expected_wait_time",
                "delay_vs_expected",
                "order_status"
            ]
        ]
    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        pass  # YOUR CODE HERE

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        pass  # YOUR CODE HERE

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
