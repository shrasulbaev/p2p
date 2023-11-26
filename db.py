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

    def count_transactions(self, type, status, start_date, end_date):
        query = """
            SELECT COUNT(*)
            FROM transaction
            WHERE type = %s
            AND status = %s
            AND date_trunc('day', created_at) BETWEEN %s AND %s
            AND agent_id = 3;
        """
        self.cursor.execute(query, (type, status, start_date, end_date))
        result = self.cursor.fetchone()[0]
        return result

    def count_all_transactions(self, type, start_date, end_date):
        query = """
            SELECT COUNT(*)
            FROM transaction
            WHERE type = %s
            AND date_trunc('day', created_at) BETWEEN %s AND %s
            AND agent_id = 3;
        """
        self.cursor.execute(query, (type, start_date, end_date))
        result = self.cursor.fetchone()[0]
        return result

    def analyze_and_write_to_file(self, output_file):
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        # Cashout Analysis
        total_cashout_yesterday = self.count_all_transactions('CASHOUT', yesterday, yesterday)
        total_cashout_today = self.count_all_transactions('CASHOUT', today, today)

        cashout_active_yesterday = self.count_transactions('CASHOUT', 'ACTIVE', yesterday, yesterday)
        cashout_completed_yesterday = self.count_transactions('CASHOUT', 'COMPLETED', yesterday, yesterday)

        cashout_active_today = self.count_transactions('CASHOUT', 'ACTIVE', today, today)
        cashout_completed_today = self.count_transactions('CASHOUT', 'COMPLETED', today, today)

        # Deposit Analysis
        total_deposit_yesterday = self.count_all_transactions('DEPOSIT', yesterday, yesterday)
        total_deposit_today = self.count_all_transactions('DEPOSIT', today, today)

        deposit_unpaid_yesterday = self.count_transactions('DEPOSIT', 'UNPAID', yesterday, yesterday)
        deposit_paid_yesterday = self.count_transactions('DEPOSIT', 'PAID', yesterday, yesterday)
        deposit_completed_yesterday = self.count_transactions('DEPOSIT', 'COMPLETED', yesterday, yesterday)

        deposit_unpaid_today = self.count_transactions('DEPOSIT', 'UNPAID', today, today)
        deposit_paid_today = self.count_transactions('DEPOSIT', 'PAID', today, today)
        deposit_completed_today = self.count_transactions('DEPOSIT', 'COMPLETED', today, today)

        with open(output_file, 'w') as file:
            # Cashout Results
            file.write(f"Total CASHOUT Transactions (Yesterday): {total_cashout_yesterday}\n")
            file.write(f"Total CASHOUT Transactions (Today): {total_cashout_today}\n")

            if total_cashout_yesterday != 0:
                file.write(f"CASHOUT ACTIVE (Yesterday): {cashout_active_yesterday} ({(cashout_active_yesterday / total_cashout_yesterday) * 100:.2f}%)\n")
                file.write(f"CASHOUT COMPLETED (Yesterday): {cashout_completed_yesterday} ({(cashout_completed_yesterday / total_cashout_yesterday) * 100:.2f}%)\n")
            else:
                file.write("CASHOUT ACTIVE (Yesterday): N/A (total_cashout_yesterday is zero, cannot calculate percentage)\n")
                file.write("CASHOUT COMPLETED (Yesterday): N/A (total_cashout_yesterday is zero, cannot calculate percentage)\n")

            if total_cashout_today != 0:
                file.write(f"CASHOUT ACTIVE (Today): {cashout_active_today} ({(cashout_active_today / total_cashout_today) * 100:.2f}%)\n")
                file.write(f"CASHOUT COMPLETED (Today): {cashout_completed_today} ({(cashout_completed_today / total_cashout_today) * 100:.2f}%)\n")
            else:
                file.write("CASHOUT ACTIVE (Today): N/A (total_cashout_today is zero, cannot calculate percentage)\n")
                file.write("CASHOUT COMPLETED (Today): N/A (total_cashout_today is zero, cannot calculate percentage)\n")

            # Deposit Results
            file.write(f"Total DEPOSIT Transactions (Yesterday): {total_deposit_yesterday}\n")
            file.write(f"Total DEPOSIT Transactions (Today): {total_deposit_today}\n")

            if total_deposit_yesterday != 0:
                file.write(f"DEPOSIT UNPAID (Yesterday): {deposit_unpaid_yesterday} ({(deposit_unpaid_yesterday / total_deposit_yesterday) * 100:.2f}%)\n")
                file.write(f"DEPOSIT PAID (Yesterday): {deposit_paid_yesterday} ({(deposit_paid_yesterday / total_deposit_yesterday) * 100:.2f}%)\n")
                file.write(f"DEPOSIT COMPLETED (Yesterday): {deposit_completed_yesterday} ({(deposit_completed_yesterday / total_deposit_yesterday) * 100:.2f}%)\n")
            else:
                file.write("DEPOSIT UNPAID (Yesterday): N/A (total_deposit_yesterday is zero, cannot calculate percentage)\n")
                file.write("DEPOSIT PAID (Yesterday): N/A (total_deposit_yesterday is zero, cannot calculate percentage)\n")
                file.write("DEPOSIT COMPLETED (Yesterday): N/A (total_deposit_yesterday is zero, cannot calculate percentage)\n")

            if total_deposit_today != 0:
                file.write(f"DEPOSIT UNPAID (Today): {deposit_unpaid_today} ({(deposit_unpaid_today / total_deposit_today) * 100:.2f}%)\n")
                file.write(f"DEPOSIT PAID (Today): {deposit_paid_today} ({(deposit_paid_today / total_deposit_today) * 100:.2f}%)\n")
                file.write(f"DEPOSIT COMPLETED (Today): {deposit_completed_today} ({(deposit_completed_today / total_deposit_today) * 100:.2f}%)\n")
            else:
                file.write("DEPOSIT UNPAID (Today): N/A (total_deposit_today is zero, cannot calculate percentage)\n")
                file.write("DEPOSIT PAID (Today): N/A (total_deposit_today is zero, cannot calculate percentage)\n")
                file.write("DEPOSIT COMPLETED (Today): N/A (total_deposit_today is zero, cannot calculate percentage)\n")

        print(f"Results written to {output_file}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

# Пример использования
if __name__ == "__main__":
    analyzer = TransactionAnalyzer(
        username='srasulbaev',
        password='FczydYjGZmU3qQmclHJazm',
        db='p2p_stage',
        host='db-p2p-stage.dats.tech',
        port=5472
    )
    analyzer.analyze_and_write_to_file('transaction_results.txt')
    analyzer.close_connection()
