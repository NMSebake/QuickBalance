import sqlite3
from pathlib import Path

from argon2 import PasswordHasher


# Database location
DATABASE_PATH = Path("data/quickbalance.db")

password_hasher = PasswordHasher()


def create_database():
    # Make sure the data directory exists
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")

    # ---------------------------------------------------------
    # CREATE CUSTOMERS TABLE
    # ---------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            id_no TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # ---------------------------------------------------------
    # CREATE ACCOUNTS TABLE
    # ---------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            account_number TEXT NOT NULL UNIQUE,
            balance INTEGER NOT NULL DEFAULT 0,
            available_balance INTEGER NOT NULL DEFAULT 0,
            acc_type TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # ---------------------------------------------------------
    # CREATE TRANSACTIONS TABLE
    # ---------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_date TEXT NOT NULL,
            description TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount INTEGER NOT NULL,

            FOREIGN KEY (account_id)
                REFERENCES accounts(account_id)
        )
    """)

    # ---------------------------------------------------------
    # MOCK CUSTOMERS - 20 ENTRIES
    # ---------------------------------------------------------

    customers = [
        ("CUST1001", "9001015800081", "thabo.m", "Thabo", "Mokoena", "Pass1001"),
        ("CUST1002", "8505125800082", "lerato.m", "Lerato", "Molefe", "Pass1002"),
        ("CUST1003", "9207235800083", "daniel.n", "Daniel", "Naidoo", "Pass1003"),
        ("CUST1004", "8804155800084", "naledi.mt", "Naledi", "Mthembu", "Pass1004"),
        ("CUST1005", "9109025800085", "sipho.d", "Sipho", "Dlamini", "Pass1005"),
        ("CUST1006", "8706205800086", "anele.k", "Anele", "Khumalo", "Pass1006"),
        ("CUST1007", "9503185800087", "kabelo.m", "Kabelo", "Mokoena", "Pass1007"),
        ("CUST1008", "8907115800088", "ayanda.n", "Ayanda", "Ndlovu", "Pass1008"),
        ("CUST1009", "9302255800089", "mpho.ma", "Mpho", "Maseko", "Pass1009"),
        ("CUST1010", "8608095800090", "zanele.z", "Zanele", "Zulu", "Pass1010"),
        ("CUST1011", "9401165800091", "neo.mo", "Neo", "Molefe", "Pass1011"),
        ("CUST1012", "9005275800092", "busisiwe.s", "Busisiwe", "Sithole", "Pass1012"),
        ("CUST1013", "8809145800093", "lungile.p", "Lungile", "Pillay", "Pass1013"),
        ("CUST1014", "9203015800094", "tshepo.mb", "Tshepo", "Mabena", "Pass1014"),
        ("CUST1015", "8507285800095", "karabo.mk", "Karabo", "Mokoena", "Pass1015"),
        ("CUST1016", "9105105800096", "siyabonga.d", "Siyabonga", "Dube", "Pass1016"),
        ("CUST1017", "9608225800097", "precious.n", "Precious", "Nkosi", "Pass1017"),
        ("CUST1018", "8701135800098", "themba.mt", "Themba", "Mthethwa", "Pass1018"),
        ("CUST1019", "9306045800099", "refilwe.mo", "Refilwe", "Modise", "Pass1019"),
        ("CUST1020", "8909255800100", "andile.c", "Andile", "Cele", "Pass1020")
    ]


    customers = [
        (
            customer_id,
            id_no,
            username,
            first_name,
            last_name,
            password_hasher.hash(password)
        )
        for (
            customer_id,
            id_no,
            username,
            first_name,
            last_name,
            password
        ) in customers
    ]

    cursor.executemany("""
        INSERT INTO customers (
            customer_id,
            id_no,
            username,
            first_name,
            last_name,
            password
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, customers)

    # ---------------------------------------------------------
    # MOCK ACCOUNTS - 60 ENTRIES
    # ---------------------------------------------------------

    accounts = [

        ("CUST1001", "1000000001", 1575050, "Cheque"),
        ("CUST1001", "2000000001", 850000, "Savings"),
        ("CUST1001", "3000000001", 450000, "Credit Card"),

        ("CUST1002", "1000000002", 842075, "Cheque"),
        ("CUST1002", "2000000002", 1250000, "Savings"),
        ("CUST1002", "3000000002", 275000, "Credit Card"),

        ("CUST1003", "1000000003", 2315000, "Cheque"),
        ("CUST1003", "2000000003", 975000, "Savings"),
        ("CUST1003", "3000000003", 625000, "Credit Card"),

        ("CUST1004", "1000000004", 1254300, "Cheque"),
        ("CUST1004", "2000000004", 1450000, "Savings"),
        ("CUST1004", "3000000004", 350000, "Credit Card"),

        ("CUST1005", "1000000005", 675250, "Cheque"),
        ("CUST1005", "2000000005", 725000, "Savings"),
        ("CUST1005", "3000000005", 200000, "Credit Card"),

        ("CUST1006", "1000000006", 1899500, "Cheque"),
        ("CUST1006", "2000000006", 2150000, "Savings"),
        ("CUST1006", "3000000006", 750000, "Credit Card"),

        ("CUST1007", "1000000007", 432100, "Cheque"),
        ("CUST1007", "2000000007", 625000, "Savings"),
        ("CUST1007", "3000000007", 300000, "Credit Card"),

        ("CUST1008", "1000000008", 987650, "Cheque"),
        ("CUST1008", "2000000008", 1125000, "Savings"),
        ("CUST1008", "3000000008", 425000, "Credit Card"),

        ("CUST1009", "1000000009", 3425000, "Cheque"),
        ("CUST1009", "2000000009", 1850000, "Savings"),
        ("CUST1009", "3000000009", 950000, "Credit Card"),

        ("CUST1010", "1000000010", 765430, "Cheque"),
        ("CUST1010", "2000000010", 950000, "Savings"),
        ("CUST1010", "3000000010", 325000, "Credit Card"),

        ("CUST1011", "1000000011", 1543200, "Cheque"),
        ("CUST1011", "2000000011", 1325000, "Savings"),
        ("CUST1011", "3000000011", 500000, "Credit Card"),

        ("CUST1012", "1000000012", 623750, "Cheque"),
        ("CUST1012", "2000000012", 875000, "Savings"),
        ("CUST1012", "3000000012", 250000, "Credit Card"),

        ("CUST1013", "1000000013", 2899500, "Cheque"),
        ("CUST1013", "2000000013", 2450000, "Savings"),
        ("CUST1013", "3000000013", 1000000, "Credit Card"),

        ("CUST1014", "1000000014", 1125800, "Cheque"),
        ("CUST1014", "2000000014", 1375000, "Savings"),
        ("CUST1014", "3000000014", 400000, "Credit Card"),

        ("CUST1015", "1000000015", 456700, "Cheque"),
        ("CUST1015", "2000000015", 525000, "Savings"),
        ("CUST1015", "3000000015", 175000, "Credit Card"),

        ("CUST1016", "1000000016", 1987650, "Cheque"),
        ("CUST1016", "2000000016", 2250000, "Savings"),
        ("CUST1016", "3000000016", 800000, "Credit Card"),

        ("CUST1017", "1000000017", 754300, "Cheque"),
        ("CUST1017", "2000000017", 925000, "Savings"),
        ("CUST1017", "3000000017", 300000, "Credit Card"),

        ("CUST1018", "1000000018", 3214500, "Cheque"),
        ("CUST1018", "2000000018", 2750000, "Savings"),
        ("CUST1018", "3000000018", 1250000, "Credit Card"),

        ("CUST1019", "1000000019", 876540, "Cheque"),
        ("CUST1019", "2000000019", 1150000, "Savings"),
        ("CUST1019", "3000000019", 375000, "Credit Card"),

        ("CUST1020", "1000000020", 1432100, "Cheque"),
        ("CUST1020", "2000000020", 1675000, "Savings"),
        ("CUST1020", "3000000020", 600000, "Credit Card")

    ]

    cursor.executemany("""
        INSERT INTO accounts (
            customer_id,
            account_number,
            balance,
            acc_type
        )
        VALUES (?, ?, ?, ?)
    """, accounts)


    # MOCK TRANSACTIONS - 300 ENTRIES
    
    transactions = [

        ("CUST1001", "Cheque", "2026-09-07", "Grocery Store", "Debit", 45000),
        ("CUST1001", "Cheque", "2026-09-06", "Salary", "Credit", 1800000),
        ("CUST1001", "Cheque", "2026-09-05", "Electricity", "Debit", 125000),
        ("CUST1001", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 100000),
        ("CUST1001", "Cheque", "2026-09-03", "Transfer Received", "Credit", 250000),
        ("CUST1001", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 100000),
        ("CUST1001", "Savings", "2026-09-06", "Interest Earned", "Credit", 12500),
        ("CUST1001", "Savings", "2026-09-05", "Online Transfer", "Debit", 50000),
        ("CUST1001", "Savings", "2026-09-04", "Cash Deposit", "Credit", 75000),
        ("CUST1001", "Savings", "2026-09-03", "Savings Contribution", "Credit", 150000),
        ("CUST1001", "Credit Card", "2026-09-07", "Restaurant", "Debit", 85000),
        ("CUST1001", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 120000),
        ("CUST1001", "Credit Card", "2026-09-05", "Card Payment", "Debit", 45000),
        ("CUST1001", "Credit Card", "2026-09-04", "Payment Received", "Credit", 200000),
        ("CUST1001", "Credit Card", "2026-09-03", "Fuel Station", "Debit", 65000),

        ("CUST1002", "Cheque", "2026-09-07", "Fuel Station", "Debit", 65000),
        ("CUST1002", "Cheque", "2026-09-06", "Salary", "Credit", 1500000),
        ("CUST1002", "Cheque", "2026-09-05", "Mobile Payment", "Debit", 35000),
        ("CUST1002", "Cheque", "2026-09-04", "Online Shopping", "Debit", 120000),
        ("CUST1002", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 500000),
        ("CUST1002", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 200000),
        ("CUST1002", "Savings", "2026-09-06", "Interest Earned", "Credit", 15000),
        ("CUST1002", "Savings", "2026-09-05", "Online Transfer", "Debit", 75000),
        ("CUST1002", "Savings", "2026-09-04", "Cash Deposit", "Credit", 100000),
        ("CUST1002", "Savings", "2026-09-03", "Savings Contribution", "Credit", 125000),
        ("CUST1002", "Credit Card", "2026-09-07", "Restaurant", "Debit", 70000),
        ("CUST1002", "Credit Card", "2026-09-06", "Fuel Station", "Debit", 55000),
        ("CUST1002", "Credit Card", "2026-09-05", "Card Payment", "Debit", 40000),
        ("CUST1002", "Credit Card", "2026-09-04", "Payment Received", "Credit", 150000),
        ("CUST1002", "Credit Card", "2026-09-03", "Online Shopping", "Debit", 95000),

        ("CUST1003", "Cheque", "2026-09-07", "Restaurant", "Debit", 85000),
        ("CUST1003", "Cheque", "2026-09-06", "Salary", "Credit", 2200000),
        ("CUST1003", "Cheque", "2026-09-05", "Water Bill", "Debit", 45000),
        ("CUST1003", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 150000),
        ("CUST1003", "Cheque", "2026-09-03", "Transfer Received", "Credit", 300000),
        ("CUST1003", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 250000),
        ("CUST1003", "Savings", "2026-09-06", "Interest Earned", "Credit", 18000),
        ("CUST1003", "Savings", "2026-09-05", "Online Transfer", "Debit", 100000),
        ("CUST1003", "Savings", "2026-09-04", "Cash Deposit", "Credit", 150000),
        ("CUST1003", "Savings", "2026-09-03", "Savings Contribution", "Credit", 200000),
        ("CUST1003", "Credit Card", "2026-09-07", "Restaurant", "Debit", 95000),
        ("CUST1003", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 180000),
        ("CUST1003", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 75000),
        ("CUST1003", "Credit Card", "2026-09-04", "Payment Received", "Credit", 250000),
        ("CUST1003", "Credit Card", "2026-09-03", "Card Payment", "Debit", 55000),

        ("CUST1004", "Cheque", "2026-09-07", "Supermarket", "Debit", 55000),
        ("CUST1004", "Cheque", "2026-09-06", "Salary", "Credit", 1750000),
        ("CUST1004", "Cheque", "2026-09-05", "Internet Bill", "Debit", 79900),
        ("CUST1004", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 80000),
        ("CUST1004", "Cheque", "2026-09-03", "Transfer Received", "Credit", 200000),
        ("CUST1004", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 175000),
        ("CUST1004", "Savings", "2026-09-06", "Interest Earned", "Credit", 16000),
        ("CUST1004", "Savings", "2026-09-05", "Online Transfer", "Debit", 85000),
        ("CUST1004", "Savings", "2026-09-04", "Cash Deposit", "Credit", 120000),
        ("CUST1004", "Savings", "2026-09-03", "Savings Contribution", "Credit", 180000),
        ("CUST1004", "Credit Card", "2026-09-07", "Restaurant", "Debit", 75000),
        ("CUST1004", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 110000),
        ("CUST1004", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 60000),
        ("CUST1004", "Credit Card", "2026-09-04", "Payment Received", "Credit", 175000),
        ("CUST1004", "Credit Card", "2026-09-03", "Card Payment", "Debit", 45000),

        ("CUST1005", "Cheque", "2026-09-07", "Fuel Station", "Debit", 70000),
        ("CUST1005", "Cheque", "2026-09-06", "Salary", "Credit", 1400000),
        ("CUST1005", "Cheque", "2026-09-05", "Airtime", "Debit", 30000),
        ("CUST1005", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 50000),
        ("CUST1005", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 150000),
        ("CUST1005", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 125000),
        ("CUST1005", "Savings", "2026-09-06", "Interest Earned", "Credit", 10000),
        ("CUST1005", "Savings", "2026-09-05", "Online Transfer", "Debit", 60000),
        ("CUST1005", "Savings", "2026-09-04", "Cash Deposit", "Credit", 90000),
        ("CUST1005", "Savings", "2026-09-03", "Savings Contribution", "Credit", 100000),
        ("CUST1005", "Credit Card", "2026-09-07", "Restaurant", "Debit", 60000),
        ("CUST1005", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 90000),
        ("CUST1005", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 50000),
        ("CUST1005", "Credit Card", "2026-09-04", "Payment Received", "Credit", 125000),
        ("CUST1005", "Credit Card", "2026-09-03", "Card Payment", "Debit", 35000),

        ("CUST1006", "Cheque", "2026-09-07", "Grocery Store", "Debit", 95000),
        ("CUST1006", "Cheque", "2026-09-06", "Salary", "Credit", 1950000),
        ("CUST1006", "Cheque", "2026-09-05", "Electricity", "Debit", 110000),
        ("CUST1006", "Cheque", "2026-09-04", "Online Shopping", "Debit", 175000),
        ("CUST1006", "Cheque", "2026-09-03", "Transfer Received", "Credit", 400000),
        ("CUST1006", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 225000),
        ("CUST1006", "Savings", "2026-09-06", "Interest Earned", "Credit", 20000),
        ("CUST1006", "Savings", "2026-09-05", "Online Transfer", "Debit", 125000),
        ("CUST1006", "Savings", "2026-09-04", "Cash Deposit", "Credit", 175000),
        ("CUST1006", "Savings", "2026-09-03", "Savings Contribution", "Credit", 250000),
        ("CUST1006", "Credit Card", "2026-09-07", "Restaurant", "Debit", 105000),
        ("CUST1006", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 150000),
        ("CUST1006", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 85000),
        ("CUST1006", "Credit Card", "2026-09-04", "Payment Received", "Credit", 300000),
        ("CUST1006", "Credit Card", "2026-09-03", "Card Payment", "Debit", 65000),

        ("CUST1007", "Cheque", "2026-09-07", "Restaurant", "Debit", 60000),
        ("CUST1007", "Cheque", "2026-09-06", "Salary", "Credit", 1350000),
        ("CUST1007", "Cheque", "2026-09-05", "Transport", "Debit", 45000),
        ("CUST1007", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 100000),
        ("CUST1007", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 100000),
        ("CUST1007", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 100000),
        ("CUST1007", "Savings", "2026-09-06", "Interest Earned", "Credit", 9000),
        ("CUST1007", "Savings", "2026-09-05", "Online Transfer", "Debit", 50000),
        ("CUST1007", "Savings", "2026-09-04", "Cash Deposit", "Credit", 75000),
        ("CUST1007", "Savings", "2026-09-03", "Savings Contribution", "Credit", 90000),
        ("CUST1007", "Credit Card", "2026-09-07", "Restaurant", "Debit", 55000),
        ("CUST1007", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 80000),
        ("CUST1007", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 45000),
        ("CUST1007", "Credit Card", "2026-09-04", "Payment Received", "Credit", 100000),
        ("CUST1007", "Credit Card", "2026-09-03", "Card Payment", "Debit", 30000),

        ("CUST1008", "Cheque", "2026-09-07", "Supermarket", "Debit", 125000),
        ("CUST1008", "Cheque", "2026-09-06", "Salary", "Credit", 1600000),
        ("CUST1008", "Cheque", "2026-09-05", "Internet Bill", "Debit", 85000),
        ("CUST1008", "Cheque", "2026-09-04", "Fuel Station", "Debit", 90000),
        ("CUST1008", "Cheque", "2026-09-03", "Transfer Received", "Credit", 250000),
        ("CUST1008", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 150000),
        ("CUST1008", "Savings", "2026-09-06", "Interest Earned", "Credit", 14000),
        ("CUST1008", "Savings", "2026-09-05", "Online Transfer", "Debit", 70000),
        ("CUST1008", "Savings", "2026-09-04", "Cash Deposit", "Credit", 125000),
        ("CUST1008", "Savings", "2026-09-03", "Savings Contribution", "Credit", 175000),
        ("CUST1008", "Credit Card", "2026-09-07", "Restaurant", "Debit", 90000),
        ("CUST1008", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 130000),
        ("CUST1008", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 70000),
        ("CUST1008", "Credit Card", "2026-09-04", "Payment Received", "Credit", 225000),
        ("CUST1008", "Credit Card", "2026-09-03", "Card Payment", "Debit", 50000),

        ("CUST1009", "Cheque", "2026-09-07", "Grocery Store", "Debit", 155000),
        ("CUST1009", "Cheque", "2026-09-06", "Salary", "Credit", 2500000),
        ("CUST1009", "Cheque", "2026-09-05", "Electricity", "Debit", 145000),
        ("CUST1009", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 200000),
        ("CUST1009", "Cheque", "2026-09-03", "Transfer Received", "Credit", 500000),
        ("CUST1009", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 300000),
        ("CUST1009", "Savings", "2026-09-06", "Interest Earned", "Credit", 25000),
        ("CUST1009", "Savings", "2026-09-05", "Online Transfer", "Debit", 150000),
        ("CUST1009", "Savings", "2026-09-04", "Cash Deposit", "Credit", 200000),
        ("CUST1009", "Savings", "2026-09-03", "Savings Contribution", "Credit", 350000),
        ("CUST1009", "Credit Card", "2026-09-07", "Restaurant", "Debit", 120000),
        ("CUST1009", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 200000),
        ("CUST1009", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 95000),
        ("CUST1009", "Credit Card", "2026-09-04", "Payment Received", "Credit", 350000),
        ("CUST1009", "Credit Card", "2026-09-03", "Card Payment", "Debit", 75000),

        ("CUST1010", "Cheque", "2026-09-07", "Fuel Station", "Debit", 80000),
        ("CUST1010", "Cheque", "2026-09-06", "Salary", "Credit", 1450000),
        ("CUST1010", "Cheque", "2026-09-05", "Mobile Payment", "Debit", 40000),
        ("CUST1010", "Cheque", "2026-09-04", "Restaurant", "Debit", 90000),
        ("CUST1010", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 200000),
        ("CUST1010", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 150000),
        ("CUST1010", "Savings", "2026-09-06", "Interest Earned", "Credit", 12000),
        ("CUST1010", "Savings", "2026-09-05", "Online Transfer", "Debit", 60000),
        ("CUST1010", "Savings", "2026-09-04", "Cash Deposit", "Credit", 100000),
        ("CUST1010", "Savings", "2026-09-03", "Savings Contribution", "Credit", 125000),
        ("CUST1010", "Credit Card", "2026-09-07", "Restaurant", "Debit", 65000),
        ("CUST1010", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 100000),
        ("CUST1010", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 55000),
        ("CUST1010", "Credit Card", "2026-09-04", "Payment Received", "Credit", 150000),
        ("CUST1010", "Credit Card", "2026-09-03", "Card Payment", "Debit", 40000),

        ("CUST1011", "Cheque", "2026-09-07", "Online Shopping", "Debit", 135000),
        ("CUST1011", "Cheque", "2026-09-06", "Salary", "Credit", 1900000),
        ("CUST1011", "Cheque", "2026-09-05", "Water Bill", "Debit", 55000),
        ("CUST1011", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 120000),
        ("CUST1011", "Cheque", "2026-09-03", "Transfer Received", "Credit", 350000),
        ("CUST1011", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 200000),
        ("CUST1011", "Savings", "2026-09-06", "Interest Earned", "Credit", 17000),
        ("CUST1011", "Savings", "2026-09-05", "Online Transfer", "Debit", 90000),
        ("CUST1011", "Savings", "2026-09-04", "Cash Deposit", "Credit", 150000),
        ("CUST1011", "Savings", "2026-09-03", "Savings Contribution", "Credit", 200000),
        ("CUST1011", "Credit Card", "2026-09-07", "Restaurant", "Debit", 85000),
        ("CUST1011", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 140000),
        ("CUST1011", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 70000),
        ("CUST1011", "Credit Card", "2026-09-04", "Payment Received", "Credit", 225000),
        ("CUST1011", "Credit Card", "2026-09-03", "Card Payment", "Debit", 55000),

        ("CUST1012", "Cheque", "2026-09-07", "Supermarket", "Debit", 75000),
        ("CUST1012", "Cheque", "2026-09-06", "Salary", "Credit", 1550000),
        ("CUST1012", "Cheque", "2026-09-05", "Airtime", "Debit", 25000),
        ("CUST1012", "Cheque", "2026-09-04", "Fuel Station", "Debit", 65000),
        ("CUST1012", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 100000),
        ("CUST1012", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 125000),
        ("CUST1012", "Savings", "2026-09-06", "Interest Earned", "Credit", 11000),
        ("CUST1012", "Savings", "2026-09-05", "Online Transfer", "Debit", 50000),
        ("CUST1012", "Savings", "2026-09-04", "Cash Deposit", "Credit", 100000),
        ("CUST1012", "Savings", "2026-09-03", "Savings Contribution", "Credit", 125000),
        ("CUST1012", "Credit Card", "2026-09-07", "Restaurant", "Debit", 60000),
        ("CUST1012", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 85000),
        ("CUST1012", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 50000),
        ("CUST1012", "Credit Card", "2026-09-04", "Payment Received", "Credit", 125000),
        ("CUST1012", "Credit Card", "2026-09-03", "Card Payment", "Debit", 35000),

        ("CUST1013", "Cheque", "2026-09-07", "Grocery Store", "Debit", 165000),
        ("CUST1013", "Cheque", "2026-09-06", "Salary", "Credit", 2300000),
        ("CUST1013", "Cheque", "2026-09-05", "Electricity", "Debit", 135000),
        ("CUST1013", "Cheque", "2026-09-04", "Online Shopping", "Debit", 220000),
        ("CUST1013", "Cheque", "2026-09-03", "Transfer Received", "Credit", 450000),
        ("CUST1013", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 275000),
        ("CUST1013", "Savings", "2026-09-06", "Interest Earned", "Credit", 23000),
        ("CUST1013", "Savings", "2026-09-05", "Online Transfer", "Debit", 125000),
        ("CUST1013", "Savings", "2026-09-04", "Cash Deposit", "Credit", 200000),
        ("CUST1013", "Savings", "2026-09-03", "Savings Contribution", "Credit", 300000),
        ("CUST1013", "Credit Card", "2026-09-07", "Restaurant", "Debit", 110000),
        ("CUST1013", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 175000),
        ("CUST1013", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 90000),
        ("CUST1013", "Credit Card", "2026-09-04", "Payment Received", "Credit", 300000),
        ("CUST1013", "Credit Card", "2026-09-03", "Card Payment", "Debit", 65000),

        ("CUST1014", "Cheque", "2026-09-07", "Restaurant", "Debit", 95000),
        ("CUST1014", "Cheque", "2026-09-06", "Salary", "Credit", 1700000),
        ("CUST1014", "Cheque", "2026-09-05", "Internet Bill", "Debit", 79900),
        ("CUST1014", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 90000),
        ("CUST1014", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 200000),
        ("CUST1014", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 175000),
        ("CUST1014", "Savings", "2026-09-06", "Interest Earned", "Credit", 15000),
        ("CUST1014", "Savings", "2026-09-05", "Online Transfer", "Debit", 80000),
        ("CUST1014", "Savings", "2026-09-04", "Cash Deposit", "Credit", 125000),
        ("CUST1014", "Savings", "2026-09-03", "Savings Contribution", "Credit", 175000),
        ("CUST1014", "Credit Card", "2026-09-07", "Restaurant", "Debit", 85000),
        ("CUST1014", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 125000),
        ("CUST1014", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 65000),
        ("CUST1014", "Credit Card", "2026-09-04", "Payment Received", "Credit", 200000),
        ("CUST1014", "Credit Card", "2026-09-03", "Card Payment", "Debit", 50000),

        ("CUST1015", "Cheque", "2026-09-07", "Fuel Station", "Debit", 55000),
        ("CUST1015", "Cheque", "2026-09-06", "Salary", "Credit", 1300000),
        ("CUST1015", "Cheque", "2026-09-05", "Transport", "Debit", 35000),
        ("CUST1015", "Cheque", "2026-09-04", "Airtime", "Debit", 20000),
        ("CUST1015", "Cheque", "2026-09-03", "Transfer Received", "Credit", 150000),
        ("CUST1015", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 100000),
        ("CUST1015", "Savings", "2026-09-06", "Interest Earned", "Credit", 8500),
        ("CUST1015", "Savings", "2026-09-05", "Online Transfer", "Debit", 45000),
        ("CUST1015", "Savings", "2026-09-04", "Cash Deposit", "Credit", 75000),
        ("CUST1015", "Savings", "2026-09-03", "Savings Contribution", "Credit", 100000),
        ("CUST1015", "Credit Card", "2026-09-07", "Restaurant", "Debit", 50000),
        ("CUST1015", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 75000),
        ("CUST1015", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 40000),
        ("CUST1015", "Credit Card", "2026-09-04", "Payment Received", "Credit", 100000),
        ("CUST1015", "Credit Card", "2026-09-03", "Card Payment", "Debit", 25000),

        ("CUST1016", "Cheque", "2026-09-07", "Supermarket", "Debit", 115000),
        ("CUST1016", "Cheque", "2026-09-06", "Salary", "Credit", 2000000),
        ("CUST1016", "Cheque", "2026-09-05", "Electricity", "Debit", 120000),
        ("CUST1016", "Cheque", "2026-09-04", "Online Shopping", "Debit", 180000),
        ("CUST1016", "Cheque", "2026-09-03", "Transfer Received", "Credit", 300000),
        ("CUST1016", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 225000),
        ("CUST1016", "Savings", "2026-09-06", "Interest Earned", "Credit", 20000),
        ("CUST1016", "Savings", "2026-09-05", "Online Transfer", "Debit", 100000),
        ("CUST1016", "Savings", "2026-09-04", "Cash Deposit", "Credit", 150000),
        ("CUST1016", "Savings", "2026-09-03", "Savings Contribution", "Credit", 225000),
        ("CUST1016", "Credit Card", "2026-09-07", "Restaurant", "Debit", 100000),
        ("CUST1016", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 150000),
        ("CUST1016", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 80000),
        ("CUST1016", "Credit Card", "2026-09-04", "Payment Received", "Credit", 275000),
        ("CUST1016", "Credit Card", "2026-09-03", "Card Payment", "Debit", 60000),

        ("CUST1017", "Cheque", "2026-09-07", "Grocery Store", "Debit", 65000),
        ("CUST1017", "Cheque", "2026-09-06", "Salary", "Credit", 1450000),
        ("CUST1017", "Cheque", "2026-09-05", "Water Bill", "Debit", 50000),
        ("CUST1017", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 75000),
        ("CUST1017", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 125000),
        ("CUST1017", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 125000),
        ("CUST1017", "Savings", "2026-09-06", "Interest Earned", "Credit", 12000),
        ("CUST1017", "Savings", "2026-09-05", "Online Transfer", "Debit", 60000),
        ("CUST1017", "Savings", "2026-09-04", "Cash Deposit", "Credit", 90000),
        ("CUST1017", "Savings", "2026-09-03", "Savings Contribution", "Credit", 125000),
        ("CUST1017", "Credit Card", "2026-09-07", "Restaurant", "Debit", 60000),
        ("CUST1017", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 85000),
        ("CUST1017", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 45000),
        ("CUST1017", "Credit Card", "2026-09-04", "Payment Received", "Credit", 125000),
        ("CUST1017", "Credit Card", "2026-09-03", "Card Payment", "Debit", 30000),

        ("CUST1018", "Cheque", "2026-09-07", "Fuel Station", "Debit", 90000),
        ("CUST1018", "Cheque", "2026-09-06", "Salary", "Credit", 2100000),
        ("CUST1018", "Cheque", "2026-09-05", "Internet Bill", "Debit", 85000),
        ("CUST1018", "Cheque", "2026-09-04", "Restaurant", "Debit", 110000),
        ("CUST1018", "Cheque", "2026-09-03", "Transfer Received", "Credit", 400000),
        ("CUST1018", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 250000),
        ("CUST1018", "Savings", "2026-09-06", "Interest Earned", "Credit", 22000),
        ("CUST1018", "Savings", "2026-09-05", "Online Transfer", "Debit", 125000),
        ("CUST1018", "Savings", "2026-09-04", "Cash Deposit", "Credit", 200000),
        ("CUST1018", "Savings", "2026-09-03", "Savings Contribution", "Credit", 275000),
        ("CUST1018", "Credit Card", "2026-09-07", "Restaurant", "Debit", 115000),
        ("CUST1018", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 175000),
        ("CUST1018", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 90000),
        ("CUST1018", "Credit Card", "2026-09-04", "Payment Received", "Credit", 300000),
        ("CUST1018", "Credit Card", "2026-09-03", "Card Payment", "Debit", 70000),

        ("CUST1019", "Cheque", "2026-09-07", "Supermarket", "Debit", 105000),
        ("CUST1019", "Cheque", "2026-09-06", "Salary", "Credit", 1650000),
        ("CUST1019", "Cheque", "2026-09-05", "Mobile Payment", "Debit", 45000),
        ("CUST1019", "Cheque", "2026-09-04", "ATM Withdrawal", "Debit", 100000),
        ("CUST1019", "Cheque", "2026-09-03", "Cash Deposit", "Credit", 175000),
        ("CUST1019", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 175000),
        ("CUST1019", "Savings", "2026-09-06", "Interest Earned", "Credit", 15000),
        ("CUST1019", "Savings", "2026-09-05", "Online Transfer", "Debit", 75000),
        ("CUST1019", "Savings", "2026-09-04", "Cash Deposit", "Credit", 125000),
        ("CUST1019", "Savings", "2026-09-03", "Savings Contribution", "Credit", 150000),
        ("CUST1019", "Credit Card", "2026-09-07", "Restaurant", "Debit", 75000),
        ("CUST1019", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 110000),
        ("CUST1019", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 60000),
        ("CUST1019", "Credit Card", "2026-09-04", "Payment Received", "Credit", 175000),
        ("CUST1019", "Credit Card", "2026-09-03", "Card Payment", "Debit", 45000),

        ("CUST1020", "Cheque", "2026-09-07", "Grocery Store", "Debit", 85000),
        ("CUST1020", "Cheque", "2026-09-06", "Salary", "Credit", 1800000),
        ("CUST1020", "Cheque", "2026-09-05", "Electricity", "Debit", 130000),
        ("CUST1020", "Cheque", "2026-09-04", "Online Shopping", "Debit", 145000),
        ("CUST1020", "Cheque", "2026-09-03", "Transfer Received", "Credit", 275000),
        ("CUST1020", "Savings", "2026-09-07", "Monthly Savings Transfer", "Credit", 200000),
        ("CUST1020", "Savings", "2026-09-06", "Interest Earned", "Credit", 18000),
        ("CUST1020", "Savings", "2026-09-05", "Online Transfer", "Debit", 100000),
        ("CUST1020", "Savings", "2026-09-04", "Cash Deposit", "Credit", 150000),
        ("CUST1020", "Savings", "2026-09-03", "Savings Contribution", "Credit", 200000),
        ("CUST1020", "Credit Card", "2026-09-07", "Restaurant", "Debit", 90000),
        ("CUST1020", "Credit Card", "2026-09-06", "Online Shopping", "Debit", 130000),
        ("CUST1020", "Credit Card", "2026-09-05", "Fuel Station", "Debit", 70000),
        ("CUST1020", "Credit Card", "2026-09-04", "Payment Received", "Credit", 225000),
        ("CUST1020", "Credit Card", "2026-09-03", "Card Payment", "Debit", 50000)

    ]

    resolved_transactions = []

    for (
        customer_id,
        account_type,
        transaction_date,
        description,
        transaction_type,
        amount
    ) in transactions:

        cursor.execute(
            """
            SELECT account_id
            FROM accounts
            WHERE customer_id = ?
            AND acc_type = ?
            """,
            (customer_id, account_type)
        )

        account = cursor.fetchone()

        if account is None:
            raise ValueError(
                f"No {account_type} account found "
                f"for customer {customer_id}"
            )

        account_id = account[0]

        resolved_transactions.append(
            (
                account_id,
                transaction_date,
                description,
                transaction_type,
                amount
            )
        )


    cursor.executemany("""
        INSERT INTO transactions (
            account_id,
            transaction_date,
            description,
            transaction_type,
            amount
            )
            VALUES (?, ?, ?, ?, ?)
        """, resolved_transactions)

    # Save all changes
    connection.commit()

    # Close connection
    connection.close()

    print("Database, tables and mock data created successfully.")


if __name__ == "__main__":
    create_database()
