import requests

class CashoutCreate:
    def __init__(self, base_url, api_key, api_sign):
        self.base_url = base_url
        self.headers = {
            'X-API-KEY': api_key,
            'X-API-SIGN': api_sign,
            'Content-Type': 'application/json'
        }

    def create_cashout(self, amount, currency, method, customer_id, email, external_transaction_id, card_number, cardholder_name, splittable):
        # Проверяем аргументы
        if any(arg is None for arg in (amount, currency, method, customer_id, email, external_transaction_id, card_number, cardholder_name, splittable)):
            raise ValueError("Неправильные аргументы. Все аргументы должны быть указаны.")

        url = f'{self.base_url}/v1/p2p/cashout/create'
        data = {
            "amount": amount,
            "currency": currency,
            "method": method,
            "customer_id": customer_id,
            "email": email,
            "external_transaction_id": external_transaction_id,
            "payment_details": {
                "card_number": card_number,
                "cardholder_name": cardholder_name
            },
            "splittable": splittable
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()  # Вызвать исключение для HTTP-ошибок (например, 404, 500)
        except requests.exceptions.RequestException as e:
            # Обработка ошибок, связанных с запросом, например, ошибок соединения
            print(f"Ошибка запроса: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            # Обработка HTTP-ошибок (например, 404, 500)
            print(f"HTTP-ошибка: {e}")
        except Exception as e:
            # Обработка других исключений
            print(f"Произошла ошибка: {e}")
            return None

        # Вывести содержимое ответа сервера
        print(response.text)  # Это выведет содержимое ответа в виде строки
        return response
