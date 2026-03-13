import requests
import json
from API_key import GOLDAPI_API_KEY

class GOLDAPI:
    def __init__(self):
        self.api_key = GOLDAPI_API_KEY
        self.curr = "USD"
        self.metal_names = {
            'XAU': 'Золото',
            'XAG': 'Серебро',
            'XPT': 'Платина',
            'XPD': 'Палладий'
        }
        self.metals = {
            "gold": "XAU",
            "silver": "XAG",
            "platinum": "XPT",
            "palladium": "XPD"
        }
        self.heads = {
            "x-access-token": self.api_key,
            "Content-Type": "application/json",
        }

    def get_metal_price(self, symbol):

        url = f"https://www.goldapi.io/api/{symbol}/{self.curr}"

        try:
            session = requests.Session()
            response = session.get(url, headers=self.heads)
            # response = requests.get(url, headers=self.heads)
            response.raise_for_status()

            result = response.json()
            ask_price = result.get('ask')

            metal_name = {
                'XAU': 'Золото',
                'XAG': 'Серебро',
                'XPT': 'Платина',
                'XPD': 'Палладий'
            }.get(symbol, symbol)
            # for name in symbol:
            return {
                'metal': metal_name,
                'ask_price': ask_price,
                'bid_price': result.get('bid'),
                'price': result.get('price')
            }
            # 'timestamp': result.get('timestamp')
        
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {symbol}:", str(e))
            return None
        
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON для {symbol}: {e}")
            return None
    
    def get_avg_of_currency(self):
        
        print('Запуск\n')

        prices = {}
        for name, code in self.metals.items():
            url = f"https://www.goldapi.io/api/{code}/{self.curr}"

            try:
                response = requests.get(url, headers=self.heads, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    prices[name] = data['price']
                    print(f"{name}: {data['price']} USD")

                else:
                    print(f"Ошибка для {name}: {response.status_code}")
                
            except Exception as e:
                print(f"Ошибка для {name}: {response.status_code}")
                return None
        
        return prices
        # return self.print_ratio_of_curr(prices)

    def print_ratio_of_curr(self, prices):

        # prices = self.get_avg_of_currency()

        if all(metal in prices for metal in ["gold", "silver", "platinum", "palladium"]):
            gold_silver = prices['gold'] / prices['silver']
            gold_platinum = prices['gold'] / prices['platinum']
            gold_palladium = prices['gold'] / prices['palladium']

            print(f"\nЗолото/серебро: {gold_silver:.2f}")
            print(f'Золото/платина: {gold_platinum:.2f}')
            print(f"Золото/палладий: {gold_palladium:.2f}")

def main():
    gold_api = GOLDAPI()
    # print(gold_api.get_metal_price('XAU'))
    gold_api.get_avg_of_currency()
    # gold_api.print_ratio_of_curr()
    
if __name__ == "__main__":
    main()