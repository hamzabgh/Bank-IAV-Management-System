def display_menu():
    """Display the main menu."""
    menu = """ 
            ********************************************************************
            *                 -- WELCOME TO BANK IARV --                       *
            *                                                                  *
            *                                                                  *
            *       1) Create Account : 1                                      *
            *       2) Login : 2                                               *
            *       3) Exit : 3                                                *
            *                                                                  *
            ********************************************************************
          """
    print(menu.center(100))

def display_user_menu(name):
    """Display the user menu."""
    user_menu = f""" 
                ********************************************************************
                *           -- WELCOME {name[0]} {name[1]} TO BANK IARV --         *
                *                                                                  *
                *                                                                  *
                *       1) Show Account :       1                                  *
                *       2) Show Transaction :   2                                  *
                *       3) deposit balance :    3                                  *
                *       4) Withdrawal Balance : 4                                  *
                *       5) Transfer Money :     5                                  *
                *       6) Dashbord Admin :     6                                  *
                *       7) Exit :               7                                  *
                *                                                                  *
                ********************************************************************                   
            """
    print(user_menu)

def display_admin_menu(name):
    """Display the user menu."""
    user_menu = f""" 
                ********************************************************************
                *          -- WELCOME {name[0]} {name[1]} TO Admin BANK IARV --    *
                *                                                                  *
                *                                                                  *
                *       1) update name :             1                             *
                *       2) update password :         2                             *
                *       3) update email :            3                             *
                *       4) activate users accounts : 4                             *
                *       5) Delete Account :          5                             *
                *       6) Exit :                    6                             *
                *                                                                  *
                ********************************************************************                   
            """
    print(user_menu)
