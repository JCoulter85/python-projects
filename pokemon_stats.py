import requests

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Pokémon not found! Please check the name.")
        return None
    
def get_weaknesses(types):
    weaknesses = set()
    for pokemon_type in types:
        type_url = pokemon_type['type']['url']  # Get the URL for the type
        response = requests.get(type_url)
        
        if response.status_code == 200:
            type_data = response.json()
            # Add weaknesses (double_damage_from types)
            for weak_type in type_data['damage_relations']['double_damage_from']:
                weaknesses.add(weak_type['name'])
        else:
            print(f"Error fetching data for type {pokemon_type['type']['name']}")
    
    return list(weaknesses)  # Convert set to list
    
pokemon_name = input("Enter Pokémon name: ")
data = get_pokemon_data(pokemon_name)

if data:
    print(f"Pokémon Name: {data['name'].capitalize()}")
    print(f"Base Experience: {data['base_experience']}")
    
def display_pokemon_stats(data):
    print("\nPokémon Details:")
    print(f"Name: {data['name'].capitalize()}")
    print(f"Base Experience: {data['base_experience']}")
    
# display types
types = data['types']  # Keep the raw list of dictionaries from the API
type_names = [t['type']['name'] for t in types]
print(f"Types: {', '.join(type_names)}")

# display stats
print("\nStats:")
for stat in data['stats']:
    print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
    
# display abilities
print("\nAbilities:")
for ability in data['abilities']:
    print(f"- {ability['ability']['name'].capitalize()}")
    
# Fetch and display weaknesses
weaknesses = get_weaknesses(types)  # Pass the raw `types` list to the function
print("\nWeaknesses:")
print(", ".join(weaknesses))

# main loop
while True:
    pokemon_name = input("\nEnter Pokémon name (or type 'quit' to exit): ").strip()
    
    if pokemon_name.lower() == "quit":
        print("Goodbye!")
        break
    data = get_pokemon_data(pokemon_name)
    
    if data:
        display_pokemon_stats(data)
    print("\nPokémon Details:")
    print(f"Name: {data['name'].capitalize()}")
    print(f"Base Experience: {data['base_experience']}")
    
    # Display types
    types = [t['type']['name'] for t in data['types']]
    print(f"Types: {', '.join(types)}")
    
    # Display stats
    print("\nStats:")
    for stat in data['stats']:
        print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
    
    # Display abilities
    print("\nAbilities:")
    for ability in data['abilities']:
        print(f"- {ability['ability']['name'].capitalize()}")