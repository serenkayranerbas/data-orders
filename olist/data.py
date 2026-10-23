from pathlib import Path
import pandas as pd


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.

    Methods:
        get_data():
            Loads and returns a dictionary where keys are dataset names (e.g., 'sellers', 'orders')
            and values are pandas DataFrames loaded from corresponding CSV files.

        ping():
            Prints "pong" to confirm the method is callable.
    """

    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        csv_path = Path.home() / ".workintech" / "olist" / "data" / "csv"
        # csv_path: CSV dosyalarının bulunduğu klasörün yolu.
        # .iterdir(): Bu klasörün içindeki dosya ve klasörleri sırayla dolaşmamızı sağlar.
        csv_files = (
            csv_path.iterdir()
        )  # iterdir() dosyaların içindeki  öğeleri listeler

        data = {}
        for file in csv_files:
            name = file.stem
            name1 = name.removeprefix("olist_")
            name_update = name1.removesuffix("_dataset")
            data[name_update] = pd.read_csv(file)
        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
