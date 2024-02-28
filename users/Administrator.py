from DB.database import Database
from users import user
from Compte import Comptes
from Transactions import Transaction

class Administrator(user.Users):
    TABLE_USER_NAME = "users"
    ID_USER_FIELD = "id_user"
    EMAIL_USER_FIELD = "email"
    PHONE_USER_FIELD = "phone"
    PASSWORD_USER_FIELD = "password"
    ISADMIN_USER_FIELD = "isadmin"
    def __init__(self, database):
        # Call the constructor of the base class (Users)
        super().__init__(database)

    def delete_account(self, user_id,user_id_to_delete):
        """
        Deletes a user account based on user ID.

        Parameters:
        - user_id: The unique identifier for the user.

        Returns:
        A success message if deletion is successful, an error message otherwise.
        """
        if not self.is_admin(user_id):
            print("Permission denied. Only administrators can delete accounts.")

        try:
            # Perform the deletion operation
            query = f"DELETE FROM {self.TABLE_NAME} WHERE {self.ID_FIELD} = %s"
            self.database.cursor.execute(query, (user_id_to_delete,))
            self.database.connection.commit()
            print(f"User account with ID {user_id_to_delete} deleted successfully.")
        except Exception as e:
            print(f"Deletion failed: {str(e)}")

    def is_admin(self,user_id):
        """
        Checks if the current user is an administrator.

        Returns:
        True if the user is an administrator, False otherwise.
        """


        query = f"SELECT {self.ISADMIN_FIELD} FROM {self.TABLE_NAME} WHERE {self.ID_FIELD} = %s"
        self.database.cursor.execute(query, (user_id,))
        is_admin = self.database.cursor.fetchone()

        # If the user is an administrator, is_admin will be a tuple (1,) or (True,)
        return is_admin and is_admin[0] == 1

    def delete_all_details_user(self, user_id, user_id_to_delete):
        """
        Deletes all details associated with a user, including transactions and accounts.

        Parameters:
        - user_id: The ID of the user initiating the deletion.
        - user_id_to_delete: The ID of the user account to be deleted.

        Returns:
        None
        """
        transaction = Transaction.TransactionsManager(self.database)
        compt = Comptes.CompteManager(self.database)

        if not self.is_admin(user_id):
            print("Permission denied. Only administrators can delete accounts.")

        try:
            # Delete transactions, account, and user details
            transaction.delete_transactions(user_id_to_delete)
            compt.delete_account(user_id_to_delete)
            self.delete_account(user_id, user_id_to_delete)
            print(f"User account with ID {user_id_to_delete} deleted successfully.")
        except Exception as e:
            print(f"Deletion failed: {str(e)}")

    def update_email_user(self, id_user, email_user_update):
        """
        Updates the email address of a user.

        Parameters:
        - id_user: The ID of the user.
        - email_user_update: The new email address for the user.

        Returns:
        None
        """
        query = f"""UPDATE {self.TABLE_USER_NAME} 
                    SET {self.EMAIL_USER_FIELD} = %s
                    WHERE {self.ID_USER_FIELD} = %s
                """
        values = (email_user_update, id_user)
        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            print("Email updated successfully.")
        except Exception as e:
            print(f"Failed to update Email: {str(e)}")

    def update_phone_user(self, id_user, phone_user_update):
        """
        Updates the phone number of a user.

        Parameters:
        - id_user: The ID of the user.
        - phone_user_update: The new phone number for the user.

        Returns:
        None
        """
        query = f"""UPDATE {self.TABLE_USER_NAME} 
                    SET {self.PHONE_USER_FIELD} = %s
                    WHERE {self.ID_USER_FIELD} = %s
                """
        values = (phone_user_update, id_user)
        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            print("Phone updated successfully.")
        except Exception as e:
            print(f"Failed to update Phone: {str(e)}")

    def update_password_user(self, id_user, password_user_update):
        """
        Updates the password of a user.

        Parameters:
        - id_user: The ID of the user.
        - password_user_update: The new password for the user.

        Returns:
        None
        """
        query = f"""UPDATE {self.TABLE_USER_NAME} 
                    SET {self.PASSWORD_USER_FIELD} = %s
                    WHERE {self.ID_USER_FIELD} = %s
                """
        hashed_password = self.hash_password(password_user_update)
        values = (hashed_password.decode('utf-8'), id_user)
        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            print("Password updated successfully.")
        except Exception as e:
            print(f"Failed to update Password: {str(e)}")