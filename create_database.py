import sqlite3
from pathlib import Path


# Database location
DATABASE_PATH = Path("data/quickbalance.db")


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

    # ---------------------------------------------------------
    # MOCK TRANSACTIONS - 100 ENTRIES
    # 5 TRANSACTIONS PER CUSTOMER
    # ---------------------------------------------------------

    transactions = [
        # CUST1001 / Account 1
        (1, "2026-09-07", "Grocery Store", "Debit", 45000),
        (1, "2026-09-06", "Salary", "Credit", 1800000),
        (1, "2026-09-05", "Electricity", "Debit", 125000),
        (1, "2026-09-04", "ATM Withdrawal", "Debit", 100000),
        (1, "2026-09-03", "Transfer Received", "Credit", 250000),

        # CUST1002 / Account 2
        (2, "2026-09-07", "Fuel Station", "Debit", 65000),
        (2, "2026-09-06", "Salary", "Credit", 1500000),
        (2, "2026-09-05", "Mobile Payment", "Debit", 35000),
        (2, "2026-09-04", "Online Shopping", "Debit", 120000),
        (2, "2026-09-03", "Cash Deposit", "Credit", 500000),

        # CUST1003 / Account 3
        (3, "2026-09-07", "Restaurant", "Debit", 85000),
        (3, "2026-09-06", "Salary", "Credit", 2200000),
        (3, "2026-09-05", "Water Bill", "Debit", 45000),
        (3, "2026-09-04", "ATM Withdrawal", "Debit", 150000),
        (3, "2026-09-03", "Transfer Received", "Credit", 300000),

        # CUST1004 / Account 4
        (4, "2026-09-07", "Supermarket", "Debit", 55000),
        (4, "2026-09-06", "Salary", "Credit", 1750000),
        (4, "2026-09-05", "Internet Bill", "Debit", 79900),
        (4, "2026-09-04", "ATM Withdrawal", "Debit", 80000),
        (4, "2026-09-03", "Transfer Received", "Credit", 200000),

        # CUST1005 / Account 5
        (5, "2026-09-07", "Fuel Station", "Debit", 70000),
        (5, "2026-09-06", "Salary", "Credit", 1400000),
        (5, "2026-09-05", "Airtime", "Debit", 30000),
        (5, "2026-09-04", "ATM Withdrawal", "Debit", 50000),
        (5, "2026-09-03", "Cash Deposit", "Credit", 150000),

        # CUST1006 / Account 6
        (6, "2026-09-07", "Grocery Store", "Debit", 95000),
        (6, "2026-09-06", "Salary", "Credit", 1950000),
        (6, "2026-09-05", "Electricity", "Debit", 110000),
        (6, "2026-09-04", "Online Shopping", "Debit", 175000),
        (6, "2026-09-03", "Transfer Received", "Credit", 400000),

        # CUST1007 / Account 7
        (7, "2026-09-07", "Restaurant", "Debit", 60000),
        (7, "2026-09-06", "Salary", "Credit", 1350000),
        (7, "2026-09-05", "Transport", "Debit", 45000),
        (7, "2026-09-04", "ATM Withdrawal", "Debit", 100000),
        (7, "2026-09-03", "Cash Deposit", "Credit", 100000),

        # CUST1008 / Account 8
        (8, "2026-09-07", "Supermarket", "Debit", 125000),
        (8, "2026-09-06", "Salary", "Credit", 1600000),
        (8, "2026-09-05", "Internet Bill", "Debit", 85000),
        (8, "2026-09-04", "Fuel Station", "Debit", 90000),
        (8, "2026-09-03", "Transfer Received", "Credit", 250000),

        # CUST1009 / Account 9
        (9, "2026-09-07", "Grocery Store", "Debit", 155000),
        (9, "2026-09-06", "Salary", "Credit", 2500000),
        (9, "2026-09-05", "Electricity", "Debit", 145000),
        (9, "2026-09-04", "ATM Withdrawal", "Debit", 200000),
        (9, "2026-09-03", "Transfer Received", "Credit", 500000),

        # CUST1010 / Account 10
        (10, "2026-09-07", "Fuel Station", "Debit", 80000),
        (10, "2026-09-06", "Salary", "Credit", 1450000),
        (10, "2026-09-05", "Mobile Payment", "Debit", 40000),
        (10, "2026-09-04", "Restaurant", "Debit", 90000),
        (10, "2026-09-03", "Cash Deposit", "Credit", 200000),

        # CUST1011 / Account 11
        (11, "2026-09-07", "Online Shopping", "Debit", 135000),
        (11, "2026-09-06", "Salary", "Credit", 1900000),
        (11, "2026-09-05", "Water Bill", "Debit", 55000),
        (11, "2026-09-04", "ATM Withdrawal", "Debit", 120000),
        (11, "2026-09-03", "Transfer Received", "Credit", 350000),

        # CUST1012 / Account 12
        (12, "2026-09-07", "Supermarket", "Debit", 75000),
        (12, "2026-09-06", "Salary", "Credit", 1550000),
        (12, "2026-09-05", "Airtime", "Debit", 25000),
        (12, "2026-09-04", "Fuel Station", "Debit", 65000),
        (12, "2026-09-03", "Cash Deposit", "Credit", 100000),

        # CUST1013 / Account 13
        (13, "2026-09-07", "Grocery Store", "Debit", 165000),
        (13, "2026-09-06", "Salary", "Credit", 2300000),
        (13, "2026-09-05", "Electricity", "Debit", 135000),
        (13, "2026-09-04", "Online Shopping", "Debit", 220000),
        (13, "2026-09-03", "Transfer Received", "Credit", 450000),

        # CUST1014 / Account 14
        (14, "2026-09-07", "Restaurant", "Debit", 95000),
        (14, "2026-09-06", "Salary", "Credit", 1700000),
        (14, "2026-09-05", "Internet Bill", "Debit", 79900),
        (14, "2026-09-04", "ATM Withdrawal", "Debit", 90000),
        (14, "2026-09-03", "Cash Deposit", "Credit", 200000),

        # CUST1015 / Account 15
        (15, "2026-09-07", "Fuel Station", "Debit", 55000),
        (15, "2026-09-06", "Salary", "Credit", 1300000),
        (15, "2026-09-05", "Transport", "Debit", 35000),
        (15, "2026-09-04", "Airtime", "Debit", 20000),
        (15, "2026-09-03", "Transfer Received", "Credit", 150000),

        # CUST1016 / Account 16
        (16, "2026-09-07", "Supermarket", "Debit", 115000),
        (16, "2026-09-06", "Salary", "Credit", 2000000),
        (16, "2026-09-05", "Electricity", "Debit", 120000),
        (16, "2026-09-04", "Online Shopping", "Debit", 180000),
        (16, "2026-09-03", "Transfer Received", "Credit", 300000),

        # CUST1017 / Account 17
        (17, "2026-09-07", "Grocery Store", "Debit", 65000),
        (17, "2026-09-06", "Salary", "Credit", 1450000),
        (17, "2026-09-05", "Water Bill", "Debit", 50000),
        (17, "2026-09-04", "ATM Withdrawal", "Debit", 75000),
        (17, "2026-09-03", "Cash Deposit", "Credit", 125000),

        # CUST1018 / Account 18
        (18, "2026-09-07", "Fuel Station", "Debit", 90000),
        (18, "2026-09-06", "Salary", "Credit", 2100000),
        (18, "2026-09-05", "Internet Bill", "Debit", 85000),
        (18, "2026-09-04", "Restaurant", "Debit", 110000),
        (18, "2026-09-03", "Transfer Received", "Credit", 400000),

        # CUST1019 / Account 19
        (19, "2026-09-07", "Supermarket", "Debit", 105000),
        (19, "2026-09-06", "Salary", "Credit", 1650000),
        (19, "2026-09-05", "Mobile Payment", "Debit", 45000),
        (19, "2026-09-04", "ATM Withdrawal", "Debit", 100000),
        (19, "2026-09-03", "Cash Deposit", "Credit", 175000),

        # CUST1020 / Account 20
        (20, "2026-09-07", "Grocery Store", "Debit", 85000),
        (20, "2026-09-06", "Salary", "Credit", 1800000),
        (20, "2026-09-05", "Electricity", "Debit", 130000),
        (20, "2026-09-04", "Online Shopping", "Debit", 145000),
        (20, "2026-09-03", "Transfer Received", "Credit", 275000)
    ]

    cursor.executemany("""
        INSERT INTO transactions (
            account_id,
            transaction_date,
            description,
            transaction_type,
            amount
        )
        VALUES (?, ?, ?, ?, ?)
    """, transactions)

    # Save all changes
    connection.commit()

    # Close connection
    connection.close()

    print("Database, tables and mock data created successfully.")


if __name__ == "__main__":
    create_database()