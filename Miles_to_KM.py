def miles_to_km(miles):
    return miles * 1.60934

def km_to_miles(km):
    return km / 1.60934

choice = input("Convert (1) Miles to Kilometers or (2) Kilometers to Miles?")

if choice == "1":
    miles = float(input("Enter miles: "))
    print (f"{miles} miles is {miles_to_km(miles):.2f} Kilometers.")
    
elif choice == "2":
    km = float(input("Enter Kilometers: "))
    print (f"{km} kilometers is {km_to_miles(km):.2f} miles.")
    
else:
    print("Invalid choice.")