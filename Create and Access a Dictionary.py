person = {"name": "Jim", "age": 39, "city": "Eugene"}
print(f"Name: {person['name']}")
print(f"Age: {person['age']}")
print(f"City: {person['city']}")

# example: Iterate Through a Dictionary
for key, value in person.items():
    print(f"{key}: {value}")