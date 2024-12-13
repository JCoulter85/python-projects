from colorama import init, Fore, Style

# Initialize Colorama for color support
init(autoreset=True)

def show_menu():
    """
    Displays the menu for the user with colored text.
    """
    print(Fore.LIGHTGREEN_EX + "\nWelcome to the ATM!" + Style.RESET_ALL)
    print(Fore.CYAN + "1. Check Balance" + Style.RESET_ALL)
    print(Fore.YELLOW + "2. Deposit Money" + Style.RESET_ALL)
    print(Fore.RED + "3. Withdraw Money" + Style.RESET_ALL)
    print(Fore.BLUE + "4. Exit" + Style.RESET_ALL)
    
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
                    balance -= withdraw_amount # I had these flipped around.
                    print(f"${withdraw_amount:.2f}has been withdrawn.")
                    print(f"Your new balance is: ${balance:.2f}")
                else:
                    print("Invalid amount. Please enter a number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        elif choice == "4":
            print("Thank you for using Jimbo's ATM. Have a lovely day!!!!!!!")
            break #forgot the break to close the app.
            
        else:
            print("Invalid choice. Please select an option from 1 - 4. Thank you...")

atm_simulator()