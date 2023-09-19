from datetime import datetime
from termcolor import colored
import threading
import requests
import time
import colorama

colorama.init()

monitor_name = "Monitor Name Here"
color_schemes = {
    "s": "green",
    "f": "red",
    "p": "cyan",
    "d": "yellow",
    "w": "white"
}


class Monitor:
    def __init__(self, n, pid, delay_ms):
        self.n = n + 1
        self.s = requests.session()

        self.delay_s = delay_ms / 1000
        self.pid = pid

    def print(self, text, status):
        print(
            colored(
                f"[{datetime.now().strftime('%m-%d-%Y %H:%M:%S')}] - "
                f"[{self.n}] - "
                f"[{monitor_name}] - "
                f"{text}",
                color_schemes.get(status)
            )
        )

    def start(self):
        while True:
            # Request headers are simply just a dictionary of identifying features about the accessing browser sent
            # to the website server.
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }
            get_products_req = self.s.get("https://blonded.co/products.json", headers=headers)

            # Checks to make sure the status code (a number that tells you the status of the request)
            # shows that the request was successful.
            if get_products_req.status_code not in [200, 201, 304]:
                self.print("Failed to access the site's product data.", "f")
                return

            all_products = get_products_req.json()["products"]

            # Searches the site's product list for the product with the monitor's given id (self.pid).
            product_data = {}
            for product in all_products:
                if product["id"] == int(self.pid):
                    product_data = product

            # If it doesn't find the product data with self.pid, continues searching until pid is located.
            if not product_data:
                self.print("Failed to find product. Monitoring...", "d")
                time.sleep(self.delay_s)
                continue

            # Prints out status of all sizes of item to user.
            self.print(f"Product loaded ({product_data['title']}). Checking stock...", "p")
            self.print("------- STOCK -------", "w")
            for variant in product_data["variants"]:
                if variant['available']:
                    self.print(f"| {variant['title']}: in stock. |", "s")
                else:
                    self.print(f"| {variant['title']}: not in stock. |", "f")
            self.print("---------------------", "w")
            time.sleep(self.delay_s)


if __name__ == '__main__':
    monitor = Monitor(0, "6693324324936", 5000)
    monitor.start()
