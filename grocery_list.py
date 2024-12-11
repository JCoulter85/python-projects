grocery_list = []

while True:
    print("\nOptions: [1] Add item [2] Remove item [3] View list [4] Quit")
    choice = input("Choose an option: ")

    if choice == "1":
        item = input("Enter item to add: ")
        grocery_list.append(item)
        print(f"Added: {item}")
    elif choice == "2":
        item = input("Enter item to remove: ")
        if item in grocery_list:
            grocery_list.remove(item)
            print(f"Removed: {item}")
        else:
            print("Item not found.")
    elif choice == "3":
        print("Grocery List:")
        for i, item in enumerate(grocery_list, 1):
            print(f"{i}. {item}")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
