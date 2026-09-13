from argon2 import PasswordHasher

from database import (
    get_customer,
    get_customer_by_id_number,
    get_online_customer,
    get_online_customer_by_customer_id,
    create_online_banking,
    link_account,
    get_linked_accounts,
    get_account,
    get_recent_transactions as db_get_recent_transactions
)

password_hasher = PasswordHasher()

def register_customer(
    id_number,
    username,
    password
):
    """
    Customer registration
    """
    if not (
        id_number
        and username
        and password
    ):
        return False, "Please complete all fields."

    customer = get_customer_by_id_number(
        id_number
    )

    if customer is None:
        return False, "ID number not found."

    if get_online_customer(username):
        return False, "Username already exists."

    if get_online_customer_by_customer_id(customer[0]):
        return False, "Customer is already registered."

    password_hash = password_hasher.hash(
        password
    )

    create_online_banking(
        customer[0],
        username,
        password_hash
    )

    return True, "Registration successful."



def hash_password(password):
    """
    Hash a password using Argon2id.

    Returns the hashed password.
    """

    return password_hasher.hash(password)


def authenticate_customer(username, password):
    """
    Authenticate a customer using username and password.

    Returns customer information if authentication succeeds.
    Returns None if authentication fails.
    """

    if not username or not password:
        return None

    username = username.strip().lower()

    customer = get_online_customer(
        # username.strip().lower()
        username
    )

    if customer is None:
        return None


    try:
        password_hasher.verify(
            customer[2],
            password
        )

    # except VerifyMismatchError:
    #     return None

    except Exception:
        return None
    
    return get_customer(customer[0])


def get_customer_accounts(customer_id):
    """
    Retrieve all accounts belonging to a customer.
    """

    customer = get_customer(customer_id)

    if customer is None:
        return []

    return get_linked_accounts(customer_id)


def get_account_dashboard(customer_id, account_id):
    """
    Retrieve customer and selected account information
    required by the dashboard.
    """

    customer = get_customer(customer_id)

    if customer is None:
        return None

    account = get_account(account_id)

    if account is None:
        return None

    # Only accounts explicitly linked to online banking are accessible.
    linked_account_ids = {
        linked_account[0]
        for linked_account in get_linked_accounts(customer_id)
    }

    if account[0] not in linked_account_ids:
        return None

    return {
        "customer_id": customer[0],
        "first_name": customer[1],
        "last_name": customer[2],
        "id_no": customer[3],

        "account_id": account[0],
        "account_number": account[2],
        "balance": account[3],
        "available_balance": account[4],
        "acc_type": account[5]
    }


def get_account_transactions(account_id, limit=5):
    """
    Retrieve the most recent transactions
    for the selected account.
    """

    return db_get_recent_transactions(
        account_id,
        limit
    )

def mini_statement(customer_id, account_id):
    """
    Generate a mini statement for the selected account.
    """

    dashboard = get_account_dashboard(
        customer_id,
        account_id
    )

    if dashboard is None:
        return None

    transactions = get_account_transactions(
        account_id,
        limit=5
    )

    return {
        "customer": {
            "customer_id": dashboard["customer_id"],
            "name": (
                f"{dashboard['first_name']} "
                f"{dashboard['last_name']}"
            ),
            "account_number": dashboard["account_number"],
            "account_type": dashboard["acc_type"]
        },
        "balance": dashboard["balance"],
        "transactions": transactions
    }



def link_customer_account(
    customer_id,
    id_number,
    account_number
):
    """
    Link an existing customer account
    to the customer's online banking profile.
    """

    customer = get_customer(
        customer_id
    )

    if customer is None:
        return False, "Customer not found."

    if customer[3] != id_number:
        return False, "ID number does not match."

    success = link_account(
        customer_id,
        account_number
    )

    if not success:
        return False, "Account not found."

    return True, "Account linked."
