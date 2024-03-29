# Bank IAV Management System

## Overview

The Bank IAV Management System is a Python-based application designed to streamline the management of bank accounts, transactions, and user information. This system simplifies tasks related to account creation, balance management, and transaction tracking.

## Features

### User Management

- Create and manage user accounts with details such as first name, last name, email, and phone number.
- Define user roles, including administrator privileges.

### Account Management

- Generate random IAV (International Account Verification) numbers for new accounts.
- Track account balances and perform balance updates.

### Transaction Handling

- Record and categorize transactions, including deposits, withdrawals, and transfers.
- View transaction history for a specific user, including sender information.

### Database Integration

- Utilizes MySQL database for persistent storage of user, account, and transaction data.

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- MySQL Database

## Getting Started

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/hamzabgh/Bank-IAV-Management-System.git
    ```

2. **Database Configuration:**
    - Set up a MySQL database and configure the connection details in `create_db.py`.

3. **Run the Application:**
    ```bash
    python main.py
    ```
