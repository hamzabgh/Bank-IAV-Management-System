from DB.database import Database
import bcrypt
import random
from Transactions import Transaction



class CompteManager:
    TABLE_NAME = "accounts"
    ID_FIELD = "id_account"
    ID_USER_FIELD = "id_user"
    RIP_FIELD = "rip_account"
    BALANCE_FIELD = "balance"

    def __init__(self, database):
        """
        Initializes the CompteManager class with a database connection.

        Parameters:
        - database: An instance of the Database class for database interaction.
        """
        self.database = database

    def create_account(self, balance=0, user_id=None):
        rip_account = self.generate_rip_account()
        query = f"INSERT INTO {self.TABLE_NAME} ({self.RIP_FIELD}, {self.BALANCE_FIELD}, {self.ID_USER_FIELD}) VALUES (%s, %s, %s)"
        values = (rip_account, balance, user_id)
        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            return f"Account created successfully."
        except Exception as e:
            return f"Failed to create account: {str(e)}"

    def update_balance(self,new_balance, id_user):
        query = f"UPDATE {self.TABLE_NAME} SET {self.BALANCE_FIELD} = {self.BALANCE_FIELD} + %s WHERE {self.ID_USER_FIELD} = %s"
        values = (new_balance, id_user)
        # print(query)
        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            print("Balance updated successfully.")
        except Exception as e:
            print(f"Failed to update balance: {str(e)}")

    def get_accounts(self):
        query = f"SELECT * FROM {self.TABLE_NAME}"
        self.database.cursor.execute(query)
        accounts = self.database.cursor.fetchall()
        print("\nListe des comptes:")
        for account in accounts:
            print(account)

    def generate_rip_account(self):
        random_rip = ''.join(random.choices('0123456789', k=24))
        return random_rip

    def get_account_by_id(self, id_user):
        """
        Retrieves the user ID based on their account_id.

        Parameters:
        - account_id: The account_id address of the user.

        Returns:
        The user ID as a tuple.
        """
        query = f"SELECT {self.RIP_FIELD},{self.BALANCE_FIELD} FROM {self.TABLE_NAME} WHERE {self.ID_USER_FIELD} = %s"
        self.database.cursor.execute(query, (id_user,))
        record = self.database.cursor.fetchone()
        if record is not None:
            return record
        else:
            print(f"Account with ID {id_user} not found.")
            return None

    def delete_account(self, account_id):
        query = f"DELETE FROM {self.TABLE_NAME} WHERE {self.ID_USER_FIELD} = %s"
        values = (account_id,)

        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            print(f"Account with ID {account_id} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete account: {str(e)}")


    def get_id_account_by_id_user(self,id_user):
        """
        Retrieves the user ID based on their account_id.

        Parameters:
        - account_id: The account_id address of the user.

        Returns:
        The user ID as a tuple.
        """
        query = f"SELECT {self.ID_FIELD} FROM {self.TABLE_NAME} WHERE {self.ID_USER_FIELD} = %s"
        self.database.cursor.execute(query, (id_user,))
        record = self.database.cursor.fetchone()
        if record is not None:
            return record
        else:
            print(f"Account ID not found.")
            return None