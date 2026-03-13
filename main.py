from API_key import GOLDAPI_API_KEY
from datetime import datetime, timedelta

import requests
import json
import time

class Currency:
    def __init__(self):
        self.api_key = GOLDAPI_API_KEY
        self.heads = {
            "x-access-token": self.api_key,
            "Content-Type": "application/json"
        }

    def get_metal_price(self, symbol, curr="USD", date=None):
        """Универсальный метод для получения цены металла"""
        try:

            if date:
                date_str = None

            start_date = datetime(2023, 1, 1)
            end_date = datetime(2023, 1, 10)

            current_date = start_date

            while current_date <= end_date:

                date_str = current_date.strftime("%Y%m%d")

                url = f"https://www.goldapi.io/api/{symbol}/{curr}/{date_str}"

            
                response = requests.get(url, headers=self.heads)
                response.raise_for_status()

                data = response.json()

                ask_price = data.get('ask')
                metal_name = {
                    'XAU': 'Золото',
                    'XAG': 'Серебро',
                    'XPT': 'Платина',
                    'XPD': 'Палладий'
                }.get(symbol, symbol)

                return {
                    'metal': metal_name,
                    'ask_price': ask_price,
                    'bid_price': data.get('bid'),
                    'price': data.get('price'),
                    'timestamp': data.get('timestamp')
                }

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {symbol}: ", str(e))
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON для {symbol}: ", str(e))
            return None
        
    def get_avg_of_currency(self):
        # metals = ['XAU', 'XAG', 'XPT', 'XPD']
        curr = "USD"
        metal_names = {
            'XAU': 'Золото',
            'XAG': 'Серебро',
            'XPT': 'Платина',
            'XPD': 'Палладий'
        }
        metals = {
        "gold": "XAU",
        "silver": "XAG",
        "platinum": "XPT",
        "palladium": "XPD"
        }
        
        print("Запуск")
        print("=" * 40)

        prices = {}
        
        for name, code in metals.items():
            url = f"https://www.goldapi.io/api/{code}/{curr}"

            try:
                response = requests.get(url, headers=self.heads, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    prices[name] = data['price']
                    print(f"{name}: {data['price']} USD")

                else:
                    print(f"Ошибка для {name}: {response.status_code}")
            except Exception as e:
                print(f"Ошибка для {name}: {e}")

            import time
            time.sleep(0.5)
        self.print_all_curr(prices)

    def print_all_curr(self, prices):
        if all(metal in prices for metal in ["gold", "silver", "platinum", "palladium"]):
            gold_silver =  prices['gold'] / prices['silver']
            gold_platinum =  prices['gold'] / prices['platinum']
            gold_palladium = prices['gold'] / prices['palladium']

            print(f"\nСоотношение")
            print(f"Золото/серебро: {gold_silver:.2f}")
            print(f"Золото/платина: {gold_platinum:.2f}")
            print(f"Золото/палладий: {gold_palladium:.2f}")


def main():
    cur = Currency()


    

if __name__ == "__main__":
    main()