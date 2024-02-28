from mysql.connector import Error

class CreateDB:
    def __init__(self, database):
        self.database = database

    # def create_db(self, new_database_name):
    #     try:
    #         self.database.connect()
    #         self.database.cursor.execute(f"CREATE DATABASE {new_database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    #         print(f"Database '{new_database_name}' created successfully")
    #     except Error as e:
    #         print("Error creating database: ", e)
    #     finally:
    #         self.database.disconnect()

    def create_db(self, new_database_name):
        try:
            self.database.connect()
            # Create database with utf8mb4_unicode_ci collation
            self.database.cursor.execute(f"CREATE DATABASE {new_database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{new_database_name}' created successfully")

            # Check privileges on the new database
            self.database.cursor.execute(f"USE {new_database_name};")
            self.database.cursor.execute("SHOW GRANTS;")
            privileges = self.database.cursor.fetchall()
            print(f"Privileges for {new_database_name}:\n")
            for privilege in privileges:
                print(privilege[0])

        except Error as e:
            print("Error creating database: ", e)
        finally:
            self.database.disconnect()
            
    def create_table_users(self, database_name):
        try:
            self.database.connect()
            query = f"""
                USE {database_name};
                CREATE TABLE IF NOT EXISTS `users` (
                    `id_user` int(11) NOT NULL AUTO_INCREMENT,
                    `firstname` varchar(50) NOT NULL,
                    `lastname` varchar(50) NOT NULL,
                    `email` varchar(255) NOT NULL,
                    `phone` varchar(60) NOT NULL,
                    `password` varchar(255) NOT NULL,
                    `isadmin` tinyint(1) DEFAULT '0',
                    PRIMARY KEY (`id_user`)
                )
                """
            self.database.cursor.execute(query)
            print("Created table 'users' successfully")
        except Error as e:
            print("Error creating users: ", e)
        finally:
            self.database.disconnect()

    def create_table_accounts(self, database_name):
        try:
            self.database.connect()
            query = f"""
                USE {database_name};
                CREATE TABLE IF NOT EXISTS `accounts` (
                    `id_account` int(11) NOT NULL AUTO_INCREMENT,
                    `rip_account` varchar(30) NOT NULL,
                    `balance` decimal(12,2) DEFAULT NULL,
                    `id_user` int(11) NOT NULL,
                    PRIMARY KEY (`id_account`)
                )
                """
            self.database.cursor.execute(query)
            print("Created table 'accounts' successfully")
        except Error as e:
            print("Error creating accounts: ", e)
        finally:
            self.database.disconnect()

    def create_table_transactions(self, database_name):
        try:
            self.database.connect()
            query = f"""
                USE {database_name};
                CREATE TABLE IF NOT EXISTS `transactions` (
                    `id_transaction` int(11) NOT NULL AUTO_INCREMENT,
                    `id_account` int(11) DEFAULT NULL,
                    `id_user` int(11) DEFAULT NULL,
                    `sender_id_user` int(11) DEFAULT NULL,
                    `amount` decimal(10,2) DEFAULT NULL,
                    `type_transactions` enum('deposit','withdrawal','transfer') DEFAULT NULL,
                    `date_transactions` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id_transaction`)
                )
                """
            self.database.cursor.execute(query)
            print("Created table 'transactions' successfully")
        except Error as e:
            print("Error creating transactions: ", e)
        finally:
            self.database.disconnect()

    def create_database_and_tables(self, new_database_name):
        try:
            self.create_db(new_database_name)
            self.create_table_users(new_database_name)
            self.create_table_accounts(new_database_name)
            self.create_table_transactions(new_database_name)
        except Error as e:
            print("Error creating database and tables: ", e)
