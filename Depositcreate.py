import requests

class DepositCreate:
    def __init__(self, base_url, api_key, api_sign):
        self.base_url = base_url
        self.headers = {
            'X-API-KEY': api_key,
            'X-API-SIGN': api_sign,
            'Content-Type': 'application/json'
        }
        self.transaction_id = None 

    def create_deposit(self, amount, currency, method, customer_id, email, external_transaction_id):
        url = f'{self.base_url}/v1/p2p/deposit/create'
        data = {
            "amount": amount,
            "currency": currency,
            "method": method,
            "customer_id": customer_id,
            "email": email,
            "external_transaction_id": external_transaction_id
        }
        response = requests.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            peers = response_data.get('peers', []) 
            if peers:
                transaction_id = peers[0].get('transaction_id')
                if transaction_id:
                    self.transaction_id = transaction_id  
                    print(f"Transaction ID: {transaction_id}")
                    return transaction_id
                else:
                    print("Transaction ID not found in the response")
            else:
                print("No 'peers' found in the response")
        else:
            print(f"Request failed with status code: {response.status_code}")

        return None


    def update_transaction(self, status, payment_proofs):
        if self.transaction_id is not None:
            url = f'{self.base_url}/v1/p2p/transaction/{self.transaction_id}/update'
            data = {
                "prolongUnpaidSiblingsSec": 0,
                "status": status,
                "payment_proofs": payment_proofs
            }
            response = requests.post(url, headers=self.headers, json=data)  
            
            if response.status_code == 200:
                print("Transaction updated successfully")
            else:
                print(f"Update transaction request failed with status code: {response.status_code}")
        else:
            print("No transaction ID available for update")
