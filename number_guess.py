import random

def number_guessing_game():
    print("Welcome to Jimbo's Number Guessing Game!")
    number_to_guess = random.randint(1, 10) # Generate random number
    user_guess = 0
    
    while user_guess != number_to_guess:
        # Get user input
        user_guess = int(input("Guess a number between 1 and 10: "))
        
        # Check if the guess is correct
        if user_guess < number_to_guess:
            print("Too low! Try again.")
        elif user_guess > number_to_guess:
            print("Too high! Try again.")
        else:
            print("Congratulations! You guessed the right number!")
            break # Exits the loop when the correct number is guessed

number_guessing_game()