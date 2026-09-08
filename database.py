import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/quickbalance.db")


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection



def get_customer(customer_id):
    """
    Retrieve a customer using their customer ID.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            first_name,
            last_name,
            id_no,
            password
        FROM customers
        WHERE customer_id = ?
    """, (customer_id,))

    customer = cursor.fetchone()

    connection.close()

    return customer



def get_accounts(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            account_id,
            customer_id,
            account_number,
            balance,
            available_balance,
            acc_type
        FROM accounts
        WHERE customer_id = ?
        ORDER BY account_id
        """,
        (customer_id,)
    )

    accounts = cursor.fetchall()

    connection.close()

    return accounts



def get_account(account_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            account_id,
            customer_id,
            account_number,
            balance,
            available_balance,
            acc_type
        FROM accounts
        WHERE account_id = ?
        """,
        (account_id,)
    )

    account = cursor.fetchone()

    connection.close()

    return account




def get_recent_transactions(account_id, limit=5):
    """
    Retrieve the most recent transactions for an account.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            transaction_id,
            transaction_date,
            description,
            transaction_type,
            amount
        FROM transactions
        WHERE account_id = ?
        ORDER BY transaction_date DESC
        LIMIT ?
    """, (account_id, limit))

    transactions = cursor.fetchall()

    connection.close()

    return transactions



def get_customer_by_username(username):
    """
    Retrieve a customer using their unique username.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            id_no,
            username,
            first_name,
            last_name,
            password
        FROM customers
        WHERE username = ?
    """, (username,))

    customer = cursor.fetchone()

    connection.close()

    return customer







def get_monthly_totals(account_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            transaction_type,
            COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE account_id = ?
        GROUP BY transaction_type
        """,
        (account_id,)
    )

    totals = cursor.fetchall()

    connection.close()

    return totals