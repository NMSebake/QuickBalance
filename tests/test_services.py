import sqlite3
import sys
from pathlib import Path

import pytest

# Allow tests to import project files from the project root
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from services import (
    authenticate_customer,
    get_account_dashboard,
    get_account_transactions,
    get_customer_accounts,
    link_customer_account,
    mini_statement,
    register_customer,
)
from database import DATABASE_PATH



LEGACY_TESTS = """
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
"""

TEST_CUSTOMER_ID = "CUST1020"
TEST_ID_NUMBER = "8909255800100"
TEST_USERNAME = "test.cust1020"
TEST_PASSWORD = "TestPassword123!"
OWN_ACCOUNT_NUMBERS = ("1000000020", "2000000020", "3000000020")


def cleanup_test_customer():
    """Remove online-banking data created by these tests."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("DELETE FROM linked_accounts WHERE customer_id = ?", (TEST_CUSTOMER_ID,))
    connection.execute("DELETE FROM online_banking WHERE customer_id = ?", (TEST_CUSTOMER_ID,))
    connection.commit()
    connection.close()


@pytest.fixture(autouse=True)
def clean_test_data():
    cleanup_test_customer()
    yield
    cleanup_test_customer()


def test_customer_has_no_linked_accounts_initially():
    assert get_customer_accounts(TEST_CUSTOMER_ID) == []


def test_nonexistent_customer_has_no_accounts():
    assert get_customer_accounts("INVALID") == []


def test_customer_can_register_for_online_banking():
    assert register_customer(TEST_ID_NUMBER, TEST_USERNAME, TEST_PASSWORD) == (True, "Registration successful.")


def test_registration_requires_valid_customer():
    assert register_customer("0000000000000", TEST_USERNAME, TEST_PASSWORD) == (False, "ID number not found.")


@pytest.mark.parametrize("id_number,username,password", [
    ("", TEST_USERNAME, TEST_PASSWORD), (TEST_ID_NUMBER, "", TEST_PASSWORD),
    (TEST_ID_NUMBER, TEST_USERNAME, ""),
])
def test_registration_requires_all_fields(id_number, username, password):
    assert register_customer(id_number, username, password)[0] is False


def test_username_must_be_unique():
    assert register_customer(TEST_ID_NUMBER, TEST_USERNAME, TEST_PASSWORD)[0] is True
    assert register_customer(TEST_ID_NUMBER, TEST_USERNAME, TEST_PASSWORD) == (False, "Username already exists.")


def test_customer_cannot_register_twice():
    assert register_customer(TEST_ID_NUMBER, TEST_USERNAME, TEST_PASSWORD)[0] is True
    assert register_customer(TEST_ID_NUMBER, "second.username", TEST_PASSWORD)[0] is False


def test_authentication_succeeds_after_registration():
    register_customer(TEST_ID_NUMBER, TEST_USERNAME, TEST_PASSWORD)
    assert authenticate_customer(TEST_USERNAME, TEST_PASSWORD) == (TEST_CUSTOMER_ID, "Andile", "Cele", TEST_ID_NUMBER)


@pytest.mark.parametrize("username,password", [(TEST_USERNAME, "WrongPassword"), ("unknown.user", TEST_PASSWORD), ("", TEST_PASSWORD), (TEST_USERNAME, "")])
def test_authentication_fails_for_invalid_credentials(username, password):
    register_customer(TEST_ID_NUMBER, TEST_USERNAME, TEST_PASSWORD)
    assert authenticate_customer(username, password) is None


def test_username_authentication_is_case_insensitive():
    register_customer(TEST_ID_NUMBER, TEST_USERNAME, TEST_PASSWORD)
    assert authenticate_customer(TEST_USERNAME.upper(), TEST_PASSWORD)[0] == TEST_CUSTOMER_ID


def test_customer_can_link_own_account():
    assert link_customer_account(TEST_CUSTOMER_ID, TEST_ID_NUMBER, OWN_ACCOUNT_NUMBERS[0]) == (True, "Account linked.")
    assert get_customer_accounts(TEST_CUSTOMER_ID)[0][2] == OWN_ACCOUNT_NUMBERS[0]


def test_customer_can_link_multiple_accounts():
    for number in OWN_ACCOUNT_NUMBERS:
        assert link_customer_account(TEST_CUSTOMER_ID, TEST_ID_NUMBER, number)[0] is True
    assert {account[2] for account in get_customer_accounts(TEST_CUSTOMER_ID)} == set(OWN_ACCOUNT_NUMBERS)


@pytest.mark.parametrize("id_number,account_number,message", [
    ("0000000000000", OWN_ACCOUNT_NUMBERS[0], "ID number does not match."),
    (TEST_ID_NUMBER, "9999999999", "Account not found."),
    (TEST_ID_NUMBER, "1000000001", "Account not found."),
])
def test_customer_cannot_link_invalid_account(id_number, account_number, message):
    assert link_customer_account(TEST_CUSTOMER_ID, id_number, account_number) == (False, message)
    assert get_customer_accounts(TEST_CUSTOMER_ID) == []


def test_customer_can_access_own_linked_account():
    link_customer_account(TEST_CUSTOMER_ID, TEST_ID_NUMBER, OWN_ACCOUNT_NUMBERS[0])
    account_id = get_customer_accounts(TEST_CUSTOMER_ID)[0][0]
    dashboard = get_account_dashboard(TEST_CUSTOMER_ID, account_id)
    assert dashboard is not None
    assert dashboard["customer_id"] == TEST_CUSTOMER_ID
    assert dashboard["account_number"] == OWN_ACCOUNT_NUMBERS[0]


@pytest.mark.parametrize("account_id", [1, 999999])
def test_customer_cannot_access_unavailable_account(account_id):
    assert get_account_dashboard(TEST_CUSTOMER_ID, account_id) is None


def test_linked_account_transactions_and_statement():
    link_customer_account(TEST_CUSTOMER_ID, TEST_ID_NUMBER, OWN_ACCOUNT_NUMBERS[0])
    account = get_customer_accounts(TEST_CUSTOMER_ID)[0]
    assert len(get_account_transactions(account[0])) == 5
    assert len(get_account_transactions(account[0], limit=2)) == 2
    statement = mini_statement(TEST_CUSTOMER_ID, account[0])
    assert statement["customer"]["account_number"] == account[2]
    assert statement["balance"] == account[3]
    assert len(statement["transactions"]) == 5


def test_each_linked_account_type_has_transactions():
    for number in OWN_ACCOUNT_NUMBERS:
        link_customer_account(TEST_CUSTOMER_ID, TEST_ID_NUMBER, number)
    assert all(len(get_account_transactions(account[0])) == 5 for account in get_customer_accounts(TEST_CUSTOMER_ID))


def test_mini_statement_cannot_access_another_customers_account():
    assert mini_statement(TEST_CUSTOMER_ID, 1) is None


