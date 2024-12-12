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
        # This will check the users balance
        print(f"Your current balance is: ${balance:.2f}")
        
        elif choice == "2":
        # This will allow the user to deposit money into their account
            try:
                deposit_amount = float(input("Enter the amount to deposit: "))
                if deposit_amount > 0:
                    balance += deposit_amount
                    print(f"${deposit_amount.2f}) has been deposited.")
                    print(f"Your new balance is: ${balance:.2f}")
                else:
                    print("Invalid amount. Please enter a positive number.")
            except ValueError:
                print("Invalid input. please enter a number.")
        