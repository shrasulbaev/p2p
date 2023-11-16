import psycopg2
from datetime import datetime, timedelta

class TransactionAnalyzer:
    def __init__(self, username, password, db, host, port):
        self.conn = psycopg2.connect(
            database=db,
            user=username,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def count_transactions(self, type, status, date):
        query = """
            SELECT COUNT(*)
            FROM transaction
            WHERE type = %s
            AND status = %s
            AND date_trunc('day', created_at) = %s;
        """
        self.cursor.execute(query, (type, status, date))
        result = self.cursor.fetchone()[0]
        return result

    def count_all_transactions(self, type, date):
        query = """
            SELECT COUNT(*)
            FROM transaction
            WHERE type = %s
            AND date_trunc('day', created_at) = %s;
        """
        self.cursor.execute(query, (type, date))
        result = self.cursor.fetchone()[0]
        return result

    def analyze_and_write_to_file(self, output_file):
        today = datetime.now().date()
        total_cashout = self.count_all_transactions('CASHOUT', today)
        total_deposit = self.count_all_transactions('DEPOSIT', today)
        cashout_active = self.count_transactions('CASHOUT', 'ACTIVE', today)
        cashout_completed = self.count_transactions('CASHOUT', 'COMPLETED', today)
        deposit_unpaid = self.count_transactions('DEPOSIT', 'UNPAID', today)
        deposit_paid = self.count_transactions('DEPOSIT', 'PAID', today)
        deposit_completed = self.count_transactions('DEPOSIT', 'COMPLETED', today)

        with open(output_file, 'w') as file:
            file.write(f"Total CASHOUT Transactions: {total_cashout}\n")
            file.write(f"Total DEPOSIT Transactions: {total_deposit}\n")
            file.write(f"CASHOUT ACTIVE: {cashout_active} ({(cashout_active / total_cashout) * 100:.2f}%)\n")
            file.write(f"CASHOUT COMPLETED: {cashout_completed} ({(cashout_completed / total_cashout) * 100:.2f}%)\n")
            file.write(f"DEPOSIT UNPAID: {deposit_unpaid} ({(deposit_unpaid / total_deposit) * 100:.2f}%)\n")
            file.write(f"DEPOSIT PAID: {deposit_paid} ({(deposit_paid / total_deposit) * 100:.2f}%)\n")
            file.write(f"DEPOSIT COMPLETED: {deposit_completed} ({(deposit_completed / total_deposit) * 100:.2f}%)\n")

        print(f"Results written to {output_file}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

# if __name__ == "__main__":
#     analyzer = TransactionAnalyzer(
#         username='srasulbaev',
#         password='FczydYjGZmU3qQmclHJazm',
#         db='p2p_stage',
#         host='db-p2p-stage.dats.tech',
#         port=5472
#     )
#     analyzer.analyze_and_write_to_file('transaction_results.txt')
#     analyzer.close_connection()
