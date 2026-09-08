from database import (
    get_customer,
    get_customer_by_username,
    get_accounts,
    get_account,
    get_recent_transactions as db_get_recent_transactions
)



def authenticate_customer(username, password):
    """
    Authenticate a customer using username and password.

    Returns customer information if authentication succeeds.
    Returns None if authentication fails.
    """

    if not username or not password:
        return None

    username = username.strip().lower()

    customer = get_customer_by_username(username)

    if customer is None:
        return None

    stored_password = customer[5]

    if password != stored_password:
        return None

    return customer



def get_customer_dashboard(customer_id):
    """
    Retrieve the customer and account information
    required for the dashboard.
    """

    customer = get_customer(customer_id)

    if customer is None:
        return None

    account = get_account(customer_id)

    if account is None:
        return None

    return {
        "customer_id": customer[0],
        "first_name": customer[1],
        "last_name": customer[2],
        "id_no": customer[3],
        "account_id": account[0],
        "account_number": account[2],
        "balance": account[3],
        "acc_type": account[4]
    }



def get_recent_transactions(customer_id, limit=5):
    """
    Retrieve the most recent transactions
    belonging to a customer.
    """

    account = get_account(customer_id)

    if account is None:
        return []

    account_id = account[0]

    return db_get_recent_transactions(account_id, limit)



def generate_mini_statement(customer_id):
    """
    Generate a mini statement for a customer.
    """

    dashboard = get_customer_dashboard(customer_id)

    if dashboard is None:
        return None

    transactions = get_recent_transactions(customer_id, limit=5)

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



def get_customer_accounts(customer_id):

    customer = get_customer(customer_id)

    if customer is None:
        return []

    return get_accounts(customer_id)



def get_account_dashboard(customer_id, account_id):

    customer = get_customer(customer_id)

    if customer is None:
        return None

    account = get_account(account_id)

    if account is None:
        return None

    # Make sure the account belongs to this customer
    if account[1] != customer_id:
        return None

    return {
        "customer_id": customer[0],
        "id_no": customer[1],
        "username": customer[2],
        "first_name": customer[3],
        "last_name": customer[4],

        "account_id": account[0],
        "account_number": account[2],
        "balance": account[3],
        "available_balance": account[4],
        "acc_type": account[5]
    }



def get_account_transactions(account_id, limit=5):

    return db_get_recent_transactions(
        account_id,
        limit
    )

# Testing automatic pytest execution