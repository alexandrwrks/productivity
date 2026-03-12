import requests
import json
import asyncio

from API_key import key

class Currency:
    def __init__(self):
        self.api_key = key
        self.heads = {
            "x-access-token": self.api_key,
            "Content-Type": "application/json"
        }

    def get_metal_price(self, symbol, curr="USD"):
        """Универсальный метод для получения цены металла"""
        url = f"https://www.goldapi.io/api/{symbol}/{curr}"

        try:
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

def main():
    cur = Currency()

    metals = ['XAU', 'XAG', 'XPT', 'XPD']
    metal_names = {
        'XAU': 'Золото',
        'XAG': 'Серебро',
        'XPT': 'Платина',
        'XPD': 'Палладий'
    }
    
    print("Запуск")
    print("=" * 40)
    
    for metal in metals:
        result = cur.get_metal_price(metal)
        if result:
            print(f"{result['metal']}:")
            print(f"  Цена покупки (Ask): ${result['ask_price']:.2f}")
            print(f"  Цена продажи (Bid): ${result['bid_price']:.2f}")
            print(f"  Средняя цена: ${result['price']:.2f}")
            print("-" * 30)
    
    print("=" * 40)

if __name__ == "__main__":
    print("Запуск")
    main()