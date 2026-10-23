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
        reviews = self.data["order_reviews"].copy()
        reviews["dim_is_one_star"] = reviews["review_score"].map(
        lambda x: 1 if x == 1 else 0
        )
        reviews["dim_is_five_star"] = reviews["review_score"].map(
            lambda x: 1 if x==5 else 0
        )        
        return reviews[["order_id", "review_score","dim_is_five_star","dim_is_one_star"]]

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        
        items = self.data["order_items"].copy()
        items = items.groupby("order_id").size().reset_index(name="number_of_items")
        return items[["number_of_items","order_id"]]
    
    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        sellers = self.data["order_items"].copy()
        sellers = sellers.groupby("order_id")["seller_id"].nunique().reset_index(name="number_of_sellers")
        return sellers[["number_of_sellers","order_id"]]

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        price = self.data["order_items"].copy()
        get_price_and_freight = price.groupby("order_id")[["price","freight_value"]].sum().reset_index()
        return get_price_and_freight

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """


    
        geo = self.data["geolocation"].copy()
        orders = self.data["orders"].copy()
        order_items = self.data["order_items"].copy()
        sellers = self.data["sellers"].copy()
        customers = self.data["customers"].copy()

        
        geo = (
            geo.groupby("geolocation_zip_code_prefix")[
                ["geolocation_lat", "geolocation_lng"]
            ]
            .mean()
            .reset_index()
        )

    
        customer_geo = customers.merge(
            geo,
            left_on="customer_zip_code_prefix",
            right_on="geolocation_zip_code_prefix",
            how="left"
        )

        customer_geo = customer_geo.rename(
            columns={
                "geolocation_lat": "customer_lat",
                "geolocation_lng": "customer_lng"
            }
        )

    
        seller_geo = sellers.merge(
            geo,
            left_on="seller_zip_code_prefix",
            right_on="geolocation_zip_code_prefix",
            how="left"
        )

        seller_geo = seller_geo.rename(
            columns={
                "geolocation_lat": "seller_lat",
                "geolocation_lng": "seller_lng"
            }
        )

        data = order_items.merge(
            seller_geo[
                ["seller_id", "seller_lat", "seller_lng"]
            ],
            on="seller_id",
            how="left"
        )

        data = data.merge(
            orders[["order_id", "customer_id"]],
            on="order_id",
            how="left"
        )

        data = data.merge(
            customer_geo[
                ["customer_id", "customer_lat", "customer_lng"]
            ],
            on="customer_id",
            how="left"
        )

        lat1 = np.radians(data["customer_lat"])
        lng1 = np.radians(data["customer_lng"])

        lat2 = np.radians(data["seller_lat"])
        lng2 = np.radians(data["seller_lng"])

        dlat = lat2 - lat1
        dlng = lng2 - lng1

        a = (
            np.sin(dlat / 2) ** 2
            + np.cos(lat1)
            * np.cos(lat2)
            * np.sin(dlng / 2) ** 2
        )

        c = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))

        data["distance_seller_customer"] = 6371 * c

        result = (
            data.groupby("order_id")["distance_seller_customer"]
            .mean()
            .reset_index()
        )

        return result
      

        
        
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
        orders = self.get_wait_time()
        reviews = self.get_review_score()
        items = self.get_number_items()
        sellers = self.get_number_sellers()
        prices = self.get_price_and_freight()
        
        training_data = orders.merge(reviews, on="order_id", how="left")
        training_data = training_data.merge(prices, on="order_id", how = "left")
        training_data = training_data.merge(items, on="order_id", how = "left")
        training_data = training_data.merge(sellers, on="order_id", how = "left")
        training_data = training_data.dropna()
        
        return training_data
