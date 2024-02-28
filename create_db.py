from DB import database
from DB.CreateDbTables import CreateDB

def create_database():
    database_name = input("Enter database name: ")
    user_database = input("Enter DATABESES username: ")
    password_database = input("Enter DATABESES password: ")
    port_database = input("Enter DATABESES port: ")

    db = database.Database(host='localhost', database='mysql', user=user_database, password=password_database, port=port_database)
    db.connect()
    create_db = CreateDB(db)

    try:
        create_db.create_database_and_tables(database_name)
    except Exception as e:
        print("Error creating database:", e)
    finally:
        db.disconnect()

if __name__ == "__main__":
    create_database()
