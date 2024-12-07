def greet_people(*names):
    for name in names:
        print(f"Hello, {name}!")
        
greet_people("Jim", "Katrina", "Abby", "Annie")