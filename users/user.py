from DB.database import Database
import bcrypt
from Compte import Comptes
from Transactions import Transaction

class Users:
    TABLE_NAME = "users"
    ID_FIELD = "id_user"
    FIRSTNAME_FIELD = "firstname"
    LASTNAME_FIELD = "lastname"
    EMAIL_FIELD = "email"
    PHONE_FIELD = "phone"
    PASSWORD_FIELD = "password"
    ISADMIN_FIELD = "isadmin"
    TYPE_TRANSACTIONS_FIELD = "type_transactions"

    def __init__(self, database):
        """
        Initializes the Users class with a database connection.

        Parameters:
        - database: An instance of the Database class for database interaction.
        """
        self.database = database

    def get_user(self, user_id):
        """
        Retrieves a user's information based on their user ID.

        Parameters:
        - user_id: The unique identifier for the user.

        Returns:
        A tuple containing user information.
        """
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {self.ID_FIELD} = %s"
        self.database.cursor.execute(query, (user_id,))
        record = self.database.cursor.fetchone()
        return record

    def get_all_user(self):
        """
        Retrieves basic user information for all users.
        """
        query = f"SELECT {self.FIRSTNAME_FIELD},{self.EMAIL_FIELD},{self.PHONE_FIELD},{self.ISADMIN_FIELD} FROM {self.TABLE_NAME}"
        self.database.cursor.execute(query)
        record = self.database.cursor.fetchall()
        print(record)

    def get_id_user(self, email):
        """
        Retrieves the user ID based on their email.

        Parameters:
        - email: The email address of the user.

        Returns:
        The user ID as a tuple.
        """
        query = f"SELECT {self.ID_FIELD} FROM {self.TABLE_NAME} WHERE {self.EMAIL_FIELD} = %s"
        self.database.cursor.execute(query, (email,))
        record = self.database.cursor.fetchone()
        return record

    def get_name_by_id_user(self, id_user):
        """
        Retrieves the user ID based on their email.

        Parameters:
        - email: The email address of the user.

        Returns:
        The user ID as a tuple.
        """
        query = f"SELECT {self.FIRSTNAME_FIELD},{self.LASTNAME_FIELD} FROM {self.TABLE_NAME} WHERE {self.ID_FIELD} = %s"
        self.database.cursor.execute(query, (id_user,))
        record = self.database.cursor.fetchone()
        return record     

    def user_exists(self, email):
        """
        Checks if a user with a given email already exists in the database.

        Parameters:
        - email: The email address to check.

        Returns:
        True if the user exists, False otherwise.
        """
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE {self.EMAIL_FIELD} = %s"
        self.database.cursor.execute(query, (email,))
        return self.database.cursor.fetchone() is not None

    def hash_password(self, password):
        """
        Hashes a password using bcrypt.

        Parameters:
        - password: The password to be hashed.

        Returns:
        The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def check_password(self, entered_password, stored_hashed_password):
        """
        Checks if the entered password matches the stored hashed password.

        Parameters:
        - entered_password: The password entered during login.
        - stored_hashed_password: The hashed password stored in the database.

        Returns:
        True if passwords match, False otherwise.
        """
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password)

    def register_user(self, firstname, lastname, email, password, phone, isadmin=False):
        """
        Registers a new user in the database.

        Parameters:
        - firstname: The user's first name.
        - lastname: The user's last name.
        - email: The user's email address.
        - password: The user's password.
        - phone: The user's phone number.
        - isadmin: A boolean indicating if the user is an administrator.

        Returns:
        A success message if registration is successful, an error message otherwise.
        """
        if self.user_exists(email):
            print(f"User with email {email} already exists.")
            return

        hashed_password = self.hash_password(password)
        query = f"INSERT INTO {self.TABLE_NAME} ({self.FIRSTNAME_FIELD}, {self.LASTNAME_FIELD}, {self.EMAIL_FIELD}, {self.PASSWORD_FIELD},{self.PHONE_FIELD},{self.ISADMIN_FIELD}) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (firstname, lastname, email, hashed_password.decode('utf-8'), phone, isadmin)
        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            return f"{firstname} {lastname} is registered successfully."
        except Exception as e:
            return f"Registration failed: {str(e)}"

    def login_user(self, email, entered_password):
        """
        Logs in a user by checking the entered password against the stored hashed password.

        Parameters:
        - email: The user's email address.
        - entered_password: The password entered during login.
        """
        query = f"SELECT {self.PASSWORD_FIELD} FROM {self.TABLE_NAME} WHERE {self.EMAIL_FIELD} = %s"
        self.database.cursor.execute(query, (email,))
        stored_hashed_password = self.database.cursor.fetchone()

        if stored_hashed_password is not None:
            stored_hashed_password = stored_hashed_password[0].encode('utf-8')
            if self.check_password(entered_password, stored_hashed_password):
                print("Login successful")
            else:
                print("Incorrect password")
        else:
            print("User not found")

    def view_profile(self, user_id):
        """
        Displays the user profile information.

        Parameters:
        - user_id: The unique identifier for the user.
        """
        user = self.get_user(user_id)
        compts = Comptes.CompteManager(self.database)
        compt_user = compts.get_account_by_id(user_id)
        if user and compt_user:
           # Get the width of the console
            console_width = 80

            # Print a centered title
            print("\nYour Account Information".center(console_width))

            # Print centered user details
            print(f"Name: {user[1]} {user[2]}".center(console_width))
            print(f"Email: {user[3]}".center(console_width))
            print(f"Balance: {compt_user[1]}".center(console_width))
            print(f"RIP: {compt_user[0]}".center(console_width))
            print(f"Phone: {user[5]}".center(console_width))
            print(f"User ID: {user[0]}".center(console_width))
            
            # Assuming there is an Account class and a method to get user accounts
            # accounts = self.get_user_accounts(user_id)
            # for account in accounts:
            #     print(f"Account ID: {account[0]}, Balance: {account[1]}")
        else:
            print("User not found")

    def get_all_transactions_user(self, id_user):
        """
        Displays the ALL Transaction information.

        Parameters:
        - id_user: The unique identifier for the user.
        """
        transaction = Transaction.TransactionsManager(self.database)
        
        if transaction:
            transaction.get_all_transactions_by_id_user(id_user)
        else:
            print(f"No transactions found for user with name {self.get_name_by_id_user(id_user)}.")

    def create_transaction_deposit_user(self, id_user, id_account, amount, type_transaction, sender_id_user=None):
        """
        Creates a deposit transaction for a user and updates the account balance.

        Parameters:
        - id_user: The ID of the user initiating the transaction.
        - id_account: The ID of the account involved in the transaction.
        - amount: The amount to deposit.
        - type_transaction: The type of transaction (deposit, withdrawal, transfer).
        - sender_id_user: The ID of the person who sent the transaction.

        Returns:
        None
        """
        compts = Comptes.CompteManager(self.database)
        transaction = Transaction.TransactionsManager(self.database)

        if type_transaction == "deposit":
            # Create a deposit transaction
            transaction_user = transaction.create_transaction(id_account, id_user, amount, "deposit", sender_id_user=None)
            print(transaction_user)
            
            # Update the account balance
            compts.update_balance(amount, id_user)
        else:
            print("..........")

    def create_transaction_withdrawal_user(self, id_user, id_account, amount, type_transaction, sender_id_user=None):
        """
        Creates a withdrawal transaction for a user and updates the account balance.

        Parameters:
        - id_user: The ID of the user initiating the transaction.
        - id_account: The ID of the account involved in the transaction.
        - amount: The amount to withdraw.
        - type_transaction: The type of transaction (deposit, withdrawal, transfer).
        - sender_id_user: The ID of the person who sent the transaction.

        Returns:
        None
        """
        compts = Comptes.CompteManager(self.database)
        transaction = Transaction.TransactionsManager(self.database)

        if type_transaction == "withdrawal":
            # Create a withdrawal transaction
            transaction_user = transaction.create_transaction(id_account, id_user, amount, "withdrawal", sender_id_user=None)
            print(transaction_user)

            # Update the account balance
            compts.update_balance(-amount, id_user)
        else:
            print("..........")

    def create_transaction_transfer_user(self, id_user, id_account, amount, type_transaction, sender_id_user):
        """
        Creates a transfer transaction for a user and updates the account balances.

        Parameters:
        - id_user: The ID of the user initiating the transaction.
        - id_account: The ID of the account involved in the transaction.
        - amount: The amount to transfer.
        - type_transaction: The type of transaction (deposit, withdrawal, transfer).
        - sender_id_user: The ID of the person who sent the transaction.

        Returns:
        None
        """
        compts = Comptes.CompteManager(self.database)
        transaction = Transaction.TransactionsManager(self.database)

        if type_transaction == "transfer":
            transaction_user = transaction.create_transaction(id_account, id_user, amount, "transfer", sender_id_user)
            print(transaction_user)

            compts.update_balance(-amount, id_user)
        else:
            print("..........")
