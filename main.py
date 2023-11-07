from Cashoutcreate import CashoutCreate
from Depositcreate import DepositCreate

api = CashoutCreate('https://api-stage-p2p-k8s.apimb.com', api_key='test', api_sign='test')

create_cashout_response = api.create_cashout(
    amount="20000.0000",
    currency="UZS",
    method="uzcard",
    customer_id="242",
    email="16972041277419908703@yahoo.com",
    external_transaction_id="12314322",
    card_number="4325038713687267",
    cardholder_name="DEMO DEPOSIT",
    splittable=True
)


deposit_creator = DepositCreate('https://api-stage-p2p-k8s.apimb.com', 'test', 'test')

transaction_id = deposit_creator.create_deposit(amount=20000, currency='UZS', method='uzcard', customer_id='123', email='example@email.com', external_transaction_id='100003')

update_status = 'PAID'
update_status2= 'COMPLETED'
update_amount_to_enroll = 20000
update_payment_proofs = [
    {
        "type": "string",
        "data": "string"
    }
]

deposit_creator.update_transaction(update_status, update_amount_to_enroll, update_payment_proofs)
deposit_creator.update_transaction(update_status2, update_amount_to_enroll, update_payment_proofs)
