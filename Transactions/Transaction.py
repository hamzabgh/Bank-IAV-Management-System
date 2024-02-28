from DB.database import Database
import random
# from prettytable import PrettyTable

class TransactionsManager:
    TABLE_NAME = "transactions"
    TABLE_ACCOUNTS_NAME = "accounts"
    TABLE_USERS_NAME = "users"
    ID_FIELD = "id_transaction"
    ID_ACCOUNT_FIELD = "id_account"
    ID_USER_FIELD = "id_user"
    SENDER_ID_USER_FIELD = "sender_id_user"
    AMOUNT_FIELD = "amount"
    TYPE_TRANSACTIONS_FIELD = "type_transactions"
    DATE_TRANSACTIONS_FIELD = "date_transactions"

    def __init__(self, database):
        """
        Initializes the TransactionsManager class with a database connection.

        Parameters:
        - database: An instance of the Database class for database interaction.
        """
        self.database = database

    def create_transaction(self, id_account, id_user , amount, type_transaction,  sender_id_user=None):
        """
        Creates a transaction record in the 'transactions' table.

        Parameters:
        - id_account: The ID of the account involved in the transaction.
        - id_user: The ID of the user initiating the transaction.
        - sender_id_user: The ID of the person who sent the transaction.
        - amount: The amount involved in the transaction.
        - type_transaction: The type of transaction (deposit, withdrawal, transfer).

        Returns:
        A message indicating the success or failure of the transaction creation.
        """
        if type_transaction not in ('deposit', 'withdrawal', 'transfer'):
            return "Invalid transaction type."

        query = f"""
            INSERT INTO {self.TABLE_NAME} 
            ({self.ID_ACCOUNT_FIELD}, {self.ID_USER_FIELD}, {self.SENDER_ID_USER_FIELD}, 
            {self.AMOUNT_FIELD}, {self.TYPE_TRANSACTIONS_FIELD})
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (id_account, id_user, sender_id_user, amount, type_transaction)

        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            return "Transaction created successfully."
        except Exception as e:
            return f"Failed to create transaction: {str(e)}"

    def get_all_transactions_by_id_user(self, id_user):
        """
        Retrieves all transactions associated with a specific user along with the sender's name.

        Parameters:
        - id_user: The ID of the user.

        Returns:
        A formatted table of transactions related to the user, including the sender's name.
        """
        query = f"""
                SELECT
                    t.{self.SENDER_ID_USER_FIELD},
                    u.firstname AS sender_name,
                    t.{self.AMOUNT_FIELD},
                    t.{self.TYPE_TRANSACTIONS_FIELD},
                    t.{self.DATE_TRANSACTIONS_FIELD}
                FROM
                    {self.TABLE_NAME} t
                left JOIN
                    {self.TABLE_USERS_NAME} u ON t.{self.SENDER_ID_USER_FIELD} = u.{self.ID_USER_FIELD}
                WHERE
                    t.{self.ID_USER_FIELD} = %s
            """
        self.database.cursor.execute(query, (id_user,))
        records = self.database.cursor.fetchall()

        if records:
            print("+----------------------+------------+------------------+---------------------+")
            print("|      Sender Name     | Amount     | Transaction Type |         Date        |")
            print("+----------------------+------------+------------------+---------------------+")

            for record in records:
                sender_name = 'You' if record[1] is None else str(record[1])
                amount = '0' if record[2] is None else f"{record[2]:.2f}"
                transaction_type = 'None' if record[3] is None else str(record[3])
                date = 'None' if record[4] is None else str(record[4])

                print(f"|{sender_name:^22}|{amount:^12}|{transaction_type:^18}|{date:^20} |")

            print("+----------------------+--------+------------------+-------------------------+")
            return records
        else:
            print(f"No transactions found for user with ID {id_user}.")
            return None


    def delete_transactions(self, id_user):
        query = f"DELETE FROM {self.TABLE_NAME} WHERE {self.ID_USER_FIELD} = %s"
        values = (id_user,)

        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            print(f"All Transaction with ID {id_user} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete Transaction: {str(e)}")
