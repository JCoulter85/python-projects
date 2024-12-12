def show_menu():
    """This will display the menu for the user"""
    print("\nWelcome to the ATM!")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdarw Money")
    print("4. Exit")
    
def atm_simulator():
    """This runs the ATM simulation."""
    balance = 1000000   # This is the starting balance of the user. :P
    
    while True:
        show_menu() # Call the def show menu so the user sees the menu
        choice = input("Enter your choice (1 - 4): ").strip()
        
        if choice == "1":
            # Check balance
            print(f"Your current balance is: ${balance:.2f}")
        
        elif choice == "2":
        # This will allow the user to deposit money into their account
            try:
                deposit_amount = float(input("Enter the amount to deposit: "))
                if deposit_amount > 0:
                    balance += deposit_amount
                    print(f"${deposit_amount:.2f} has been deposited.")
                    print(f"Your new balance is: ${balance:.2f}")
                else:
                    print("Invalid amount. Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        elif choice == "3":
            try:
                withdraw_amount = float(input("Enter the amount to withdraw: "))
                if withdraw_amount > balance:
                    print("Insufficient funds. Please try a smaller amount.")
                elif withdraw_amount > 0:
                    withdraw_amount -= balance
                    print(f"${withdraw_amount:.2f}has been withdrawn.")
                    print(f"Your new balance is: ${balance:.2f}")
                else:
                    print("Invalid amount. Please enter a number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == 4:
            print("Thank you for using Jimbo's ATM. Have a lovely day!!!!!!!")
            
        else:
            print("Invalid choice. Please select an option from 1 - 4. Thank you...")

atm_simulator()