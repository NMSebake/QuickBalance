import io
from pathlib import Path

import pandas as pd
import streamlit as st

from openpyxl.styles import Font, Alignment

from services import (
    authenticate_customer,
    get_customer_dashboard,
    get_recent_transactions,
    generate_mini_statement
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="QuickBalance",
    page_icon="🏦",
    layout="centered"
)


# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    css_file = Path("styles.css")

    with open(css_file, "r", encoding="utf-8") as file:
        css = file.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "customer_id" not in st.session_state:
    st.session_state.customer_id = None


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.title("🏦 QuickBalance")

    st.subheader("Customer Self-Service")

    st.write(
        "Access your account balance, recent transactions "
        "and mini statement."
    )

    st.divider()

    username = st.text_input(
        "Username",
        placeholder="Enter your username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    login_button = st.button(
        "Login",
        type="primary",
        use_container_width=True
    )

    if login_button:

        if not username or not password:

            st.error(
                "Please enter your username and password."
            )

            return

        customer = authenticate_customer(
            username,
            password
        )

        if customer is None:

            st.error(
                "Invalid username or password."
            )

            return

        st.session_state.authenticated = True
        st.session_state.customer_id = customer[0]

        st.rerun()


# =========================================================
# ACCOUNT CARD
# =========================================================

def display_account_card(dashboard):

    first_name = dashboard["first_name"]
    last_name = dashboard["last_name"]

    account_number = dashboard["account_number"]
    account_type = dashboard["acc_type"]

    balance = dashboard["balance"]
    balance_rands = balance / 100

    with st.container(
        key="account_card"
    ):

        st.caption("QuickBalance")

        st.markdown(
            f"Account number: **{account_number}**"
        )

        st.success(
            "Available Balance"
        )

        st.markdown(
            f"## R{balance_rands:,.2f}"
        )

        holder_column, type_column = st.columns(2)

        with holder_column:

            st.caption("Account holder")

            st.markdown(
                f"**{first_name} {last_name}**"
            )

        with type_column:

            st.caption("Account type")

            st.markdown(
                f"**{account_type}**"
            )


# =========================================================
# TRANSACTION ROW
# =========================================================

def display_transaction(transaction):

    (
        transaction_id,
        transaction_date,
        description,
        transaction_type,
        amount
    ) = transaction

    amount_rands = amount / 100

    if transaction_type == "Credit":

        icon = "↑"

        amount_display = (
            f"+R{amount_rands:,.2f}"
        )

        badge = "Income"

        row_class = "credit"

    else:

        icon = "↓"

        amount_display = (
            f"-R{amount_rands:,.2f}"
        )

        badge = "Payment"

        row_class = "debit"

    with st.container(
        border=True
    ):

        icon_column, information_column, amount_column = st.columns(
            [0.7, 4, 1.5],
            vertical_alignment="center"
        )

        with icon_column:

            st.markdown(
                f"### {icon}"
            )

        with information_column:

            st.markdown(
                f"**{description.upper()}**"
            )

            st.caption(
                f"{transaction_date}  •  {badge}"
            )

        with amount_column:

            st.markdown(
                f"**{amount_display}**"
            )


# =========================================================
# RECENT TRANSACTIONS
# =========================================================

def display_recent_transactions(transactions):

    with st.container(
        key="transactions_card"
    ):

        header_column, count_column = st.columns(
            [4, 1],
            vertical_alignment="center"
        )

        with header_column:

            st.subheader(
                "Recent transactions"
            )

        with count_column:

            st.caption(
                "Last 5"
            )

        if not transactions:

            st.info(
                "No recent transactions found."
            )

            return

        for transaction in transactions:

            display_transaction(transaction)


# =========================================================
# THIS MONTH
# =========================================================

def display_monthly_summary(transactions):

    money_in = sum(
        transaction[4]
        for transaction in transactions
        if transaction[3] == "Credit"
    )

    money_out = sum(
        transaction[4]
        for transaction in transactions
        if transaction[3] == "Debit"
    )

    money_in_rands = money_in / 100
    money_out_rands = money_out / 100

    with st.container(
        key="monthly_card"
    ):

        st.caption("THIS MONTH")

        income_column, income_value = st.columns(
            [2, 1]
        )

        with income_column:

            st.write("Money in")

        with income_value:

            st.markdown(
                f"**+R{money_in_rands:,.2f}**"
            )

        st.divider()

        expense_column, expense_value = st.columns(
            [2, 1]
        )

        with expense_column:

            st.write("Money out")

        with expense_value:

            st.markdown(
                f"**-R{money_out_rands:,.2f}**"
            )


# =========================================================
# MINI STATEMENT
# =========================================================

def create_excel_statement(statement):

    statement_data = []

    for transaction in statement["transactions"]:

        (
            transaction_id,
            transaction_date,
            description,
            transaction_type,
            amount
        ) = transaction

        statement_data.append(
            {
                "Date": transaction_date,
                "Description": description,
                "Transaction Type": transaction_type,
                "Amount (R)": amount / 100
            }
        )

    statement_df = pd.DataFrame(
        statement_data
    )

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        statement_df.to_excel(
            writer,
            index=False,
            sheet_name="Mini Statement",
            startrow=7
        )

        worksheet = writer.sheets[
            "Mini Statement"
        ]

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        worksheet["A1"] = "QUICKBALANCE"

        worksheet["A1"].font = Font(
            bold=True,
            size=20
        )

        worksheet["A2"] = "Mini Statement"

        worksheet["A2"].font = Font(
            bold=True,
            size=14
        )

        # -------------------------------------------------
        # CUSTOMER INFORMATION
        # -------------------------------------------------

        worksheet["A4"] = "Customer Name"
        worksheet["B4"] = statement["customer"]["name"]

        worksheet["A5"] = "Account Number"
        worksheet["B5"] = (
            statement["customer"]["account_number"]
        )

        worksheet["A6"] = "Account Type"
        worksheet["B6"] = (
            statement["customer"]["account_type"]
        )

        worksheet["C4"] = "Current Balance"

        worksheet["D4"] = (
            statement["balance"] / 100
        )

        for cell in [
            "A4",
            "A5",
            "A6",
            "C4"
        ]:

            worksheet[cell].font = Font(
                bold=True
            )

        worksheet["D4"].number_format = (
            "R #,##0.00"
        )

        worksheet["D4"].font = Font(
            bold=True
        )

        # -------------------------------------------------
        # TRANSACTION TABLE
        # -------------------------------------------------

        header_row = 8

        for cell in worksheet[header_row]:

            cell.font = Font(
                bold=True
            )

            cell.alignment = Alignment(
                horizontal="center"
            )

        for row in range(
            header_row + 1,
            worksheet.max_row + 1
        ):

            worksheet.cell(
                row=row,
                column=4
            ).number_format = (
                "R #,##0.00"
            )

        # -------------------------------------------------
        # FILTER + FREEZE
        # -------------------------------------------------

        worksheet.auto_filter.ref = (
            f"A{header_row}:"
            f"D{worksheet.max_row}"
        )

        worksheet.freeze_panes = "A9"

        # -------------------------------------------------
        # COLUMN WIDTHS
        # -------------------------------------------------

        worksheet.column_dimensions["A"].width = 15
        worksheet.column_dimensions["B"].width = 30
        worksheet.column_dimensions["C"].width = 22
        worksheet.column_dimensions["D"].width = 18

    return output.getvalue()


# =========================================================
# DOCUMENTS
# =========================================================

def display_documents(statement, account_number):

    excel_data = create_excel_statement(
        statement
    )

    with st.container(
        key="documents_card"
    ):

        st.caption("DOCUMENTS")

        st.markdown(
            "**Mini Statement**"
        )

        st.write(
            "View or download your latest mini statement."
        )

        st.download_button(
            label="Download Statement",
            data=excel_data,
            file_name=(
                f"xxxxxxx"
                f"{account_number[-4:]}.xlsx"
            ),
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True,
            key="download_statement"
        )


# =========================================================
# DASHBOARD PAGE
# =========================================================

def dashboard_page():

    customer_id = st.session_state.customer_id

    dashboard = get_customer_dashboard(
        customer_id
    )

    if dashboard is None:

        st.error(
            "Unable to retrieve customer information."
        )

        return

    transactions = get_recent_transactions(
        customer_id,
        limit=5
    )

    # -----------------------------------------------------
    # ACCOUNT
    # -----------------------------------------------------

    display_account_card(
        dashboard
    )

    # -----------------------------------------------------
    # MAIN DASHBOARD
    # -----------------------------------------------------

    left_column, right_column = st.columns(
        [2.2, 1],
        gap="medium"
    )

    with left_column:

        display_recent_transactions(
            transactions
        )

    with right_column:

        display_monthly_summary(
            transactions
        )

        statement = generate_mini_statement(
            customer_id
        )

        if statement is not None:

            display_documents(
                statement,
                dashboard["account_number"]
            )

    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    if st.button(
        "Logout",
        use_container_width=True,
        key="logout_button"
    ):

        st.session_state.authenticated = False
        st.session_state.customer_id = None

        st.rerun()


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if not st.session_state.authenticated:

    login_page()

else:

    dashboard_page()