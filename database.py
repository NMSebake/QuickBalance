import os
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(
    os.environ.get(
        "QUICKBALANCE_DATABASE_PATH",
        "data/quickbalance.db",
    )
)


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection



def get_customer(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            customer_id,
            first_name,
            last_name,
            id_no
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



def get_customer_by_id_number(id_number):
    """
    Find customr by ID number
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM customers
        WHERE id_no=?
        """,
        (id_number,)
    )

    customer = cursor.fetchone()

    connection.close()

    return customer



def get_online_customer(username):
    """
    Check customer username
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM online_banking
        WHERE username=?
        """,
        (username.lower(),)
    )

    customer = cursor.fetchone()

    connection.close()

    return customer


def get_online_customer_by_customer_id(customer_id):
    """Return the online-banking profile for a customer, if one exists."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM online_banking
        WHERE customer_id = ?
        """,
        (customer_id,),
    )

    customer = cursor.fetchone()
    connection.close()
    return customer



def create_online_banking(
    customer_id,
    username,
    password_hash
):
    """
    Create online banking profile
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO online_banking
        VALUES (?,?,?)
        """,
        (
            customer_id,
            username.lower(),
            password_hash
        )
    )

    connection.commit()

    connection.close()



def link_account(
    customer_id,
    account_number
):
    """
    Link account
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT account_id
        FROM accounts
        WHERE customer_id=?
        AND account_number=?
        """,
        (
            customer_id,
            account_number
        )
    )

    account = cursor.fetchone()

    if account is None:

        connection.close()

        return False

    cursor.execute(
        """
        INSERT OR IGNORE INTO linked_accounts
        VALUES (?,?)
        """,
        (
            customer_id,
            account[0]
        )
    )

    connection.commit()

    connection.close()

    return True



def get_linked_accounts(customer_id):
    """
    Get linked account
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT a.*
        FROM accounts a

        JOIN linked_accounts l

        ON a.account_id=l.account_id

        WHERE l.customer_id=?
        """,
        (customer_id,)
    )

    accounts = cursor.fetchall()

    connection.close()

    return accounts
