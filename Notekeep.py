filename = "notes.txt"

while True:
    print("\nOptions: [1] Write note [2] View notes [3] Quit")
    choice = input("Choose an option: ")

    if choice == "1":
        note = input("Enter your note: ")
        with open(filename, "a") as file:
            file.write(note + "\n")
        print("Note saved.")
    elif choice == "2":
        print("\nYour Notes:")
        try:
            with open(filename, "r") as file:
                for line in file:
                    print(f"- {line.strip()}")
        except FileNotFoundError:
            print("No notes found.")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")