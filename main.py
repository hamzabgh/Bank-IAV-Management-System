from DB.database import Database
from users import user,Administrator
from Compte import Comptes    
from menu import display_admin_menu,display_menu,display_user_menu
import os



def main():
    db = Database(host='localhost', database='banck_iarv', user='root', password='', port='3306')
    db.connect()
    users = user.Users(database=db)
    admin = Administrator.Administrator(database=db)
    compts = Comptes.CompteManager(database=db)

    try:
        while True:
            display_menu()
            user_input = int(input("Enter your choice: "))

            if user_input == 1:
                # Registration process
                firstname = input("Enter your first name: ")
                lastname = input("Enter your last name: ")
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                phone = input("Enter your phone: ")
                register_user = users.register_user(firstname, lastname, email, password, phone)
                print(register_user)
                if "successfully" in register_user:
                    id_user = users.get_id_user(email)[0]
                    create_compt = compts.create_account(user_id=id_user)
                    print(create_compt)
                else:
                    print("Failed to register user.")

            elif user_input == 2:
                # Login process
                email_login = input("Enter your email: ")
                password_login = input("Enter your password: ")
                if users.user_exists(email_login):
                    users.login_user(email_login, password_login)
                    id_user = users.get_id_user(email_login)[0]
                    id_acount = compts.get_id_account_by_id_user(id_user)[0]
                    user_name = users.get_name_by_id_user(id_user)
                    while True:
                        display_user_menu(user_name)
                        input1 = int(input("Enter what you want: "))

                        if input1 == 1:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            users.view_profile(id_user)
                        elif input1 == 2:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            users.get_all_transactions_user(id_user)
                            pass
                        elif input1 == 3:
                            os.system('cls' if os.name == 'nt' else 'clear')

                            new_balance = int(input("Deposit balance: "))
                            users.create_transaction_deposit_user(id_user,id_acount,new_balance,"deposit")
                            pass
                        elif input1 == 4:
                            os.system('cls' if os.name == 'nt' else 'clear')

                            withdrawal_balnce = int(input("How much to withdrawal: "))
                            users.create_transaction_withdrawal_user(id_user,id_acount,withdrawal_balnce,"withdrawal")
                            pass
                        elif input1 == 5:
                            os.system('cls' if os.name == 'nt' else 'clear')

                            transfer_balnce = int(input("How mach to transfer: "))
                            rip_user = int(input("RIB user : "))
                            users.create_transaction_transfer_user(id_user,id_acount,transfer_balnce,"transfer",rip_user)
                            pass
                        elif input1 == 6:
                            # Check if the current user is an administrator
                            os.system('cls' if os.name == 'nt' else 'clear')
                            if admin.is_admin(id_user):
                                while True :
                                    display_admin_menu(user_name)
                                    input_admin = int(input("Enter your choice: "))
                                    if input_admin == 1:
                                        pass
                                    elif input_admin == 2:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        id_user_for_update = int(input("Entare Id user: "))
                                        password_user_update = input("Entare new Password: ")
                                        admin.update_password_user(id_user_for_update,password_user_update)
                                    elif input_admin == 3:
                                        os.system('cls' if os.name == 'nt' else 'clear')
                                        id_user_for_update = int(input("Entare Id user: "))
                                        email_user_update = input("Entare new Email: ")
                                        admin.update_email_user(id_user_for_update,email_user_update)
                                    elif input_admin == 4:
                                        pass
                                    elif input_admin == 5:
                                        user_id_to_delete = int(input("Enter the user ID to delete: "))
                                        admin.delete_all_details_user(id_user,user_id_to_delete)
                                    else :
                                        print("Admin Exiting...")
                                        break
                            else:
                                print("Permission denied. Only administrators can delete accounts.")    
                        elif input1 == 7:
                            print("Exiting...")
                            break
                        else:
                            break
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("User not found.")

            elif user_input == 3:
                
                print("Exiting...")
                break

            else:
                print('Invalid option. Please try again.')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    db.disconnect()

if __name__ == "__main__":
    main()

