import sys
from pathlib import Path

# Allow tests to import project files from the project root
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from services import (
    get_customer_accounts,
    get_account_dashboard,
    get_account_transactions
)


def test_customer_has_three_accounts():

    accounts = get_customer_accounts("CUST1001")

    assert len(accounts) == 3

    account_types = {
        account[5]
        for account in accounts
    }

    assert account_types == {
        "Cheque",
        "Savings",
        "Credit Card"
    }


def test_nonexistent_customer_has_no_accounts():

    accounts = get_customer_accounts("INVALID")

    assert accounts == []


def test_customer_can_access_own_account():

    accounts = get_customer_accounts("CUST1001")

    account_id = accounts[0][0]

    dashboard = get_account_dashboard(
        "CUST1001",
        account_id
    )

    assert dashboard is not None

    assert dashboard["customer_id"] == "CUST1001"
    assert dashboard["account_id"] == account_id


def test_customer_cannot_access_another_customers_account():

    customer_one_accounts = get_customer_accounts("CUST1001")

    customer_two_accounts = get_customer_accounts("CUST1002")

    customer_two_account_id = customer_two_accounts[0][0]

    dashboard = get_account_dashboard(
        "CUST1001",
        customer_two_account_id
    )

    assert dashboard is None


def test_nonexistent_account_returns_none():

    dashboard = get_account_dashboard(
        "CUST1001",
        999999
    )

    assert dashboard is None


def test_account_transactions_are_returned():

    accounts = get_customer_accounts("CUST1001")

    account_id = accounts[0][0]

    transactions = get_account_transactions(
        account_id
    )

    assert len(transactions) == 5


def test_transaction_limit_works():

    accounts = get_customer_accounts("CUST1001")

    account_id = accounts[0][0]

    transactions = get_account_transactions(
        account_id,
        limit=2
    )

    assert len(transactions) == 2