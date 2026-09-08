# QuickBalance — Customer Self-Service Banking App

## 1. Project Overview

**QuickBalance** is a prototype customer self-service banking application developed as part of a software developer interview case study.

The purpose of the application is to reduce low-value branch and contact-centre interactions by allowing customers to perform simple banking enquiries themselves.

The application allows a customer to:

* Log in using a mock Customer ID.
* View their current account balance.
* View their five most recent transactions.
* Request and view a mini statement.
* Export the mini statement as a simple file.

The application uses **Python** for the application logic and **SQLite** for storing mock customer, account, and transaction data.

---

# 2. Business Problem

Customers frequently visit bank branches or contact the call centre for simple requests such as:

* Checking their account balance.
* Viewing recent transactions.
* Requesting a mini statement.

These interactions consume staff time and increase customer waiting times.

QuickBalance demonstrates how a simple self-service application could allow customers to perform these activities independently.

---

# 3. Project Objectives

The main objectives of the prototype are to:

1. Provide customers with a simple self-service interface.
2. Retrieve customer account information from a database.
3. Display the customer's current balance.
4. Display the five most recent transactions.
5. Generate a basic mini statement.
6. Demonstrate input validation and error handling.
7. Demonstrate awareness of banking application security requirements.
8. Apply the Software Development Life Cycle (SDLC) to the development process.

---

# 4. Features

## 4.1 Mock Customer Login

Customers enter a Customer ID to access their account.

Example:

```text
Customer ID: CUST1001
```

Authentication is mocked because the case study does not provide access to a real authentication service.

Invalid Customer IDs are handled gracefully and do not expose customer information.

---

## 4.2 Account Balance

After successful login, the customer can view their current account balance.

Example:

```text
Available Balance

R15,750.50
```

The balance is retrieved from the SQLite database rather than being hard-coded into the interface.

---

## 4.3 Recent Transactions

The application retrieves and displays the customer's five most recent transactions.

Example:

| Date       | Description       | Type   |     Amount |
| ---------- | ----------------- | ------ | ---------: |
| 2026-09-07 | Grocery Store     | Debit  |    R450.00 |
| 2026-09-06 | Salary            | Credit | R18,000.00 |
| 2026-09-05 | Electricity       | Debit  |  R1,250.00 |
| 2026-09-04 | ATM Withdrawal    | Debit  |  R1,000.00 |
| 2026-09-03 | Transfer Received | Credit |  R2,500.00 |

Transactions are ordered by transaction date, with the most recent transactions displayed first.

---

## 4.4 Mini Statement

The customer can request a mini statement containing their recent account activity.

The statement can be:

* Displayed within the application.
* Exported as a simple CSV file.

The exported statement contains relevant transaction information such as:

* Transaction date.
* Description.
* Transaction type.
* Amount.

---

# 5. Technology Stack

| Component             | Technology       |
| --------------------- | ---------------- |
| Programming Language  | Python           |
| User Interface        | Streamlit        |
| Database              | SQLite           |
| Database Connectivity | Python `sqlite3` |
| Data Processing       | Pandas           |
| Testing               | Pytest           |
| Version Control       | Git              |

### Why Python?

Python was selected because it provides:

* Clear and readable syntax.
* Strong database support.
* A large ecosystem of libraries.
* Fast development for a prototype.
* Good support for testing and data processing.

### Why SQLite?

SQLite was selected because:

* It is lightweight.
* It does not require a separate database server.
* It is built into Python.
* It supports relational database concepts.
* It is appropriate for a small prototype with mock data.

For a production banking application, SQLite would likely be replaced with an enterprise-grade database depending on the bank's architecture and requirements.

### Why Streamlit?

Streamlit allows the application to provide a functional web interface while keeping the implementation primarily in Python.

This makes it suitable for demonstrating the application's functionality during an interview.

---

# 6. Software Development Life Cycle

The project follows the Software Development Life Cycle (SDLC).

## Phase 1 — Planning

The business problem was identified as the high volume of simple customer enquiries handled through branches and contact centres.

The initial scope was limited to:

* Customer login.
* Balance enquiry.
* Recent transactions.
* Mini statement.

Complex banking functionality such as payments and transfers was deliberately excluded.

---

## Phase 2 — Requirements Analysis

### Functional Requirements

The application must:

* Allow a customer to enter a Customer ID.
* Validate the Customer ID.
* Retrieve the customer's account.
* Display the current account balance.
* Retrieve the customer's transactions.
* Display the five most recent transactions.
* Generate a mini statement.
* Allow the statement to be exported.
* Display an appropriate error message for an invalid Customer ID.

### Non-Functional Requirements

The application should:

* Be easy to use.
* Protect customer information.
* Validate user input.
* Handle errors gracefully.
* Provide consistent results.
* Be maintainable and modular.
* Separate presentation, business logic, and data access where practical.

---

# 7. System Architecture

The prototype follows a simple layered architecture:

```text
                    CUSTOMER
                       |
                       v
              +----------------+
              |  Streamlit UI  |
              +----------------+
                       |
                       v
              +----------------+
              | Business Logic |
              |    Python      |
              +----------------+
                       |
                       v
              +----------------+
              | SQLite Database|
              +----------------+
                       |
                       v
              +----------------+
              | Mock Banking   |
              |     Data       |
              +----------------+
```

### Presentation Layer

Responsible for:

* Login screen.
* Dashboard.
* Balance display.
* Transaction table.
* Mini statement interface.
* User messages.

### Business Logic Layer

Responsible for:

* Customer validation.
* Retrieving account information.
* Retrieving recent transactions.
* Preparing statement data.

### Data Layer

Responsible for:

* Connecting to SQLite.
* Executing database queries.
* Retrieving customer, account and transaction data.

---

# 8. Database Design

The prototype uses SQLite as its relational database.

The main entities are:

```text
CUSTOMERS
    |
    | 1
    |
    | *
ACCOUNTS
    |
    | 1
    |
    | *
TRANSACTIONS
```

## Customers

Stores customer information.

Example fields:

```text
customer_id
first_name
last_name
```

## Accounts

Stores account information.

Example fields:

```text
account_id
customer_id
account_number
balance
```

## Transactions

Stores account transaction information.

Example fields:

```text
transaction_id
account_id
transaction_date
description
transaction_type
amount
```

Foreign keys are used to establish relationships between customers, accounts and transactions.

---

# 9. Mock Data

Because the application cannot connect to a real banking system, a SQLite database containing fictional data is used.

Example:

```text
Customer ID: CUST1001
Name: John Doe
Account: ****1234
Balance: R15,750.50
```

All customer names, account numbers and transactions used by the application are fictional.

No real customer information should be added to this project.

---

# 10. Security Considerations

Although authentication is mocked for this prototype, security was considered during the design.

A production banking application would require significantly stronger security controls.

Potential production controls would include:

* Multi-factor authentication (MFA).
* Strong password/PIN policies.
* Secure session management.
* Role-based access control.
* Encryption in transit using HTTPS/TLS.
* Encryption of sensitive data at rest where appropriate.
* Parameterized SQL queries to prevent SQL injection.
* Input validation and sanitization.
* Rate limiting and account lockout controls.
* Secure logging and audit trails.
* Protection against session hijacking.
* Secure secrets and credential management.
* Data minimisation.
* Appropriate masking of account numbers.
* Monitoring and fraud detection.

For example, account numbers should not normally be displayed in full:

```text
****1234
```

The prototype intentionally uses mock authentication because implementing real authentication is outside the scope of the case study.

---

# 11. Input Validation

The application should validate user input before processing it.

For example:

```text
Empty Customer ID
        ↓
Display validation message
        ↓
Do not query the database
```

For an invalid Customer ID:

```text
Customer enters:
CUST9999

        ↓

Database lookup

        ↓

Customer not found

        ↓

Display:
"Customer ID not found."
```

The application should avoid displaying technical database errors directly to customers.

---

# 12. Error Handling

The application is designed to handle common errors gracefully.

Examples include:

| Scenario                     | Expected Behaviour                                        |
| ---------------------------- | --------------------------------------------------------- |
| Empty Customer ID            | Display validation message                                |
| Invalid Customer ID          | Display customer-friendly error                           |
| Database unavailable         | Display appropriate error message                         |
| No transactions              | Display an appropriate message                            |
| Statement generation failure | Inform the user that the statement could not be generated |

Technical details should be logged appropriately rather than exposed to the customer.

---

# 13. Testing Strategy

Testing will be performed at multiple levels.

## Unit Testing

Individual functions can be tested independently.

Examples:

```text
test_customer_exists()
test_get_balance()
test_get_recent_transactions()
test_generate_statement()
```

## Integration Testing

Test the interaction between:

```text
Python Application
        ↓
SQLite Database
```

For example:

* Customer login retrieves the correct customer.
* Balance retrieval returns the correct account.
* Transaction retrieval returns the correct five transactions.

## User Acceptance Testing

The complete application can be tested from the customer's perspective.

Example:

```text
Login
  ↓
View balance
  ↓
View recent transactions
  ↓
Request mini statement
  ↓
Export statement
```

---

# 14. Example Test Cases

| Test Case         | Input          | Expected Result                 |
| ----------------- | -------------- | ------------------------------- |
| Valid login       | `CUST1001`     | Customer dashboard displayed    |
| Invalid login     | `CUST9999`     | Error message displayed         |
| Empty login       | Empty value    | Validation message displayed    |
| Balance retrieval | Valid customer | Correct balance displayed       |
| Transactions      | Valid customer | Latest 5 transactions displayed |
| Mini statement    | Valid customer | Statement generated             |
| Statement export  | Valid customer | CSV file generated              |

---

# 15. Project Structure

The project is organised into separate components to improve maintainability.

```text
QuickBalance/
│
├── app.py
├── database.py
├── create_database.py
├── services.py
├── auth.py
│
├── data/
│   └── quickbalance.db
│
├── exports/
│   └── statements/
│
├── tests/
│   └── test_services.py
│
├── requirements.txt
└── README.md
```

### Key Files

**`app.py`**

Contains the Streamlit user interface.

**`database.py`**

Handles the SQLite database connection and database-related operations.

**`services.py`**

Contains the application's business logic.

**`auth.py`**

Handles the prototype authentication process.

**`create_database.py`**

Creates the database tables and inserts mock data.

**`tests/`**

Contains automated tests.

---

# 16. Installation

## Prerequisites

Install:

* Python 3.x
* pip
* Git (optional)

Check the Python installation:

```bash
python --version
```

---

# 17. Setup

Clone or copy the project:

```bash
git clone <repository-url>
cd QuickBalance
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# 18. Create the Database

Run:

```bash
python create_database.py
```

This will:

1. Create the SQLite database.
2. Create the required tables.
3. Insert fictional customers.
4. Insert fictional accounts.
5. Insert fictional transactions.

---

# 19. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in a browser.

---

# 20. Demo Customer

A fictional customer can be used for demonstration.

Example:

```text
Customer ID: CUST1001
```

Other demo Customer IDs can be added to the database as required.

---

# 21. Assumptions

The following assumptions were made:

1. Each customer has a unique Customer ID.
2. Each customer has at least one account.
3. The prototype focuses on a single account per customer.
4. Transactions are stored in SQLite.
5. Authentication is mocked.
6. No real banking systems are available.
7. All customer and transaction information is fictional.
8. The mini statement is based on the available transaction data.
9. The application is intended as a prototype rather than a production banking system.

---

# 22. Scope

## In Scope

* Mock customer login.
* Account balance enquiry.
* Five most recent transactions.
* Mini statement.
* Statement export.
* SQLite database.
* Input validation.
* Error handling.
* Basic automated testing.

## Out of Scope

* Real customer authentication.
* OTP/MFA.
* Money transfers.
* Payments.
* Beneficiary management.
* Account opening.
* Real banking API integration.
* Real customer data.
* Production deployment.
* Full fraud detection.

---

# 23. Possible Future Improvements

If this application were developed further, I would consider:

### Authentication

Replace mock authentication with a secure authentication service including MFA.

### Banking Integration

Integrate with the bank's authorised backend services or APIs rather than accessing a local database.

### Database

Move from SQLite to an enterprise database appropriate for the bank's infrastructure.

### Security

Implement:

* MFA.
* Encryption.
* Secure session management.
* Role-based access control.
* Audit logging.
* Rate limiting.

### User Experience

Add:

* Transaction search.
* Transaction filtering.
* Date-range filtering.
* Responsive design.
* Accessibility improvements.

### Scalability

For thousands or millions of customers, the application could be deployed using a scalable backend architecture with:

* Load balancing.
* Multiple application instances.
* Enterprise database infrastructure.
* Caching where appropriate.
* Monitoring and logging.
* Automated deployment pipelines.

---

# 24. Stretch Goals

The following features can be added if additional development time is available:

* [ ] Transaction search.
* [ ] Transaction filtering.
* [ ] Automated tests.
* [ ] Docker containerisation.
* [ ] Cloud deployment.
* [ ] Improved authentication.
* [ ] Additional account types.
* [ ] PDF mini statement generation.
* [ ] Application logging.
* [ ] API layer.

---

# 25. What I Learned

This project demonstrates the process of taking a business problem and translating it into a working software solution.

The main areas demonstrated are:

* Requirements analysis.
* SDLC methodology.
* Python development.
* Relational database design.
* SQL queries.
* Data validation.
* Error handling.
* Testing.
* Basic application security.
* Separation of application responsibilities.
* Consideration of scalability and maintainability.

---

# 26. Interview Summary

QuickBalance was designed with the SDLC in mind rather than starting directly with coding.

I first identified the business problem and defined the scope. I then translated the requirements into functional and non-functional requirements before designing the database and application structure.

Python was selected for the application logic, SQLite for the prototype database, and Streamlit for the user interface.

The application uses fictional data to simulate a banking environment and demonstrates the core customer self-service functionality requested in the case study.

Although authentication is mocked, security considerations were incorporated into the design, with production considerations such as MFA, encryption, secure sessions, audit logging and access control identified as future requirements.

With more time, I would focus on strengthening authentication and security, adding automated testing, introducing an API layer, improving the user experience, and designing the solution for production-scale deployment.
