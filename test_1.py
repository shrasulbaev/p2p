from Cashoutcreate import CashoutCreate
from Depositcreate import DepositCreate
import time
import random
from db import TransactionAnalyzer
import concurrent.futures
import asyncio


analyzer = TransactionAnalyzer(
    username='srasulbaev',
    password='FczydYjGZmU3qQmclHJazm',
    db='p2p_stage',
    host='db-p2p-stage.dats.tech',
    port=5472
)

# Cashout
# customers_ids_cashout = [str(random.randint(1, 5000)) for _ in range(4000)]
# amounts_cashout = 20000
# api_cashout = CashoutCreate('https://api-stage-p2p-k8s.apimb.com', api_key='auto', api_sign='auto')

# with open('request_log_cashout.txt', 'w') as log_file_cashout:
#     for customer_id in customers_ids_cashout:
#         amount = amounts_cashout
#         splittable = False
#         external_transaction_id_cashout = f"1000{random.randint(0, 999)}"

#         start_time = time.time()
#         create_cashout_response = api_cashout.create_cashout(
#             amount=amount,
#             currency="UZS",
#             method="uzcard",
#             customer_id=customer_id,
#             email="16972041277419908703@yahoo.com",
#             external_transaction_id=external_transaction_id_cashout,
#             card_number="4325038713687267",
#             cardholder_name="DEMO DEPOSIT",
#             splittable=splittable
#         )
#         end_time = time.time()
#         execution_time = end_time - start_time

#         log_file_cashout.write(f"Создание вывода\n")
#         log_file_cashout.write(f"customer_id {customer_id}: время выполнения {execution_time} секунд\n")

#         if create_cashout_response is not None:
#             log_file_cashout.write(f"Статус транзакции: {create_cashout_response.status_code}\n")
#             log_file_cashout.write(f"Ответ сервера: {create_cashout_response.text}\n")
#         else:
#             log_file_cashout.write("Ошибка\n")

        # time.sleep(1)


# Deposit
api_deposit = DepositCreate('https://api-stage-p2p-k8s.apimb.com', 'auto', 'auto')
customers_ids_deposit = [str(random.randint(5001, 99999)) for _ in range(4000)]
max_concurrent_deposits = 10

async def process_customer_deposit(customer_id):
    email_deposit = f"example@email.com"
    external_transaction_id_deposit = f"1000{random.randint(0, 999)}"
    amount_deposit = 20000

    start_time_deposit = time.time()
    transaction_id_deposit = api_deposit.create_deposit(
        amount=amount_deposit,
        currency='UZS',
        method='uzcard',
        customer_id=customer_id,
        email=email_deposit,
        external_transaction_id=external_transaction_id_deposit
    )
    end_time_deposit = time.time()
    execution_time_deposit = end_time_deposit - start_time_deposit

    with open('request_log_deposit.txt', 'a') as log_file_deposit:
        log_file_deposit.write(f"Создание депозита\n")
        log_file_deposit.write(f"customer_id {customer_id}: время выполнения {execution_time_deposit} секунд\n")

        if transaction_id_deposit is not None:
            log_file_deposit.write(f"Ответ сервера: {transaction_id_deposit}\n")
            log_file_deposit.write(f"Номер: {transaction_id_deposit}\n")

            update_status_deposit = 'PAID'
            update_payment_proofs_deposit = [{"type": "string", "data": "string"}]
            api_deposit.update_transaction(update_status_deposit, update_payment_proofs_deposit)

            update_status_completed = 'COMPLETED'
            api_deposit.update_transaction(update_status_completed, update_payment_proofs_deposit)

async def main():
    tasks = [process_customer_deposit(customer_id) for customer_id in customers_ids_deposit]

    semaphore = asyncio.Semaphore(max_concurrent_deposits)
    async with semaphore:
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

analyzer.analyze_and_write_to_file('transaction_results.txt')

analyzer.close_connection()

