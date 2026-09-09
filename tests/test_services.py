import sys
from pathlib import Path

# Allow tests to import project files from the project root
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from services import (
    authenticate_customer,
    get_customer_accounts,
    get_account_dashboard,
    get_account_transactions,
    mini_statement
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



def test_mini_statement_returns_selected_account_details():
    accounts = get_customer_accounts("CUST1001")
    account_id = accounts[0][0]

    statement = mini_statement(
        "CUST1001",
        account_id
    )

    assert statement is not None

    assert statement["customer"]["customer_id"] == "CUST1001"
    assert statement["customer"]["account_number"] == accounts[0][2]
    assert statement["customer"]["account_type"] == accounts[0][5]

    assert statement["balance"] == accounts[0][3]

    assert len(statement["transactions"]) == 5



def test_mini_statement_cannot_access_another_customers_account():
    customer_one_accounts = get_customer_accounts("CUST1001")
    customer_two_accounts = get_customer_accounts("CUST1002")

    customer_two_account_id = customer_two_accounts[0][0]

    statement = mini_statement(
        "CUST1001",
        customer_two_account_id
    )

    assert statement is None



def test_authentication_succeeds_with_correct_password():
    customer = authenticate_customer(
        "thabo.m",
        "Pass1001"
    )

    assert customer is not None
    assert customer[0] == "CUST1001"
    assert customer[2] == "thabo.m"



def test_authentication_fails_with_wrong_password():
    customer = authenticate_customer(
        "thabo.m",
        "WrongPassword"
    )

    assert customer is None



def test_authentication_fails_for_unknown_username():
    customer = authenticate_customer(
        "unknown.user",
        "Pass1001"
    )

    assert customer is None



def test_authentication_fails_with_missing_credentials():
    assert authenticate_customer(
        "",
        "Pass1001"
    ) is None

    assert authenticate_customer(
        "thabo.m",
        ""
    ) is None



def test_each_account_type_has_transactions():

    accounts = get_customer_accounts("CUST1001")

    for account in accounts:

        account_id = account[0]

        transactions = get_account_transactions(
            account_id
        )

        assert len(transactions) == 5