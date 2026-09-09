import sys
import sqlite3
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from database import DATABASE_PATH


def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def test_customer_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )

    count = cursor.fetchone()[0]

    connection.close()

    assert count == 20


def test_account_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM accounts"
    )

    count = cursor.fetchone()[0]

    connection.close()

    assert count == 60


def test_transaction_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    count = cursor.fetchone()[0]

    connection.close()

    assert count == 300


def test_three_accounts_per_customer():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            customer_id,
            COUNT(*)
        FROM accounts
        GROUP BY customer_id
        """
    )

    results = cursor.fetchall()

    connection.close()

    assert len(results) == 20

    for customer_id, account_count in results:

        assert account_count == 3


def test_account_types():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            acc_type,
            COUNT(*)
        FROM accounts
        GROUP BY acc_type
        """
    )

    results = dict(
        cursor.fetchall()
    )

    connection.close()

    assert results["Cheque"] == 20
    assert results["Savings"] == 20
    assert results["Credit Card"] == 20


def test_unique_account_numbers():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(account_number),
            COUNT(DISTINCT account_number)
        FROM accounts
        """
    )

    total, unique = cursor.fetchone()

    connection.close()

    assert total == unique


def test_no_orphan_accounts():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM accounts a
        LEFT JOIN customers c
            ON a.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    )

    orphan_count = cursor.fetchone()[0]

    connection.close()

    assert orphan_count == 0


def test_no_orphan_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM transactions t
        LEFT JOIN accounts a
            ON t.account_id = a.account_id
        WHERE a.account_id IS NULL
        """
    )

    orphan_count = cursor.fetchone()[0]

    connection.close()

    assert orphan_count == 0


def test_each_account_has_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            account_id,
            COUNT(*)
        FROM transactions
        GROUP BY account_id
        """
    )

    results = cursor.fetchall()

    connection.close()

    assert len(results) == 60

    for account_id, transaction_count in results:
        assert transaction_count == 5



def test_each_customer_has_five_transactions_per_account():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            a.customer_id,
            a.acc_type,
            COUNT(t.transaction_id)
        FROM accounts a
        LEFT JOIN transactions t
            ON a.account_id = t.account_id
        GROUP BY
            a.customer_id,
            a.acc_type
        ORDER BY
            a.customer_id,
            a.acc_type
        """
    )

    results = cursor.fetchall()

    connection.close()

    assert len(results) == 60

    for customer_id, account_type, transaction_count in results:
        assert transaction_count == 5



