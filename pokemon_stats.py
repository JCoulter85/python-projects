import requests

def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Pokémon not found! Please check the name.")
        return None
    
pokemon_name = input("Enter Pokémon name: ")
data = get_pokemon_data(pokemon_name)

if data:
    print(f"Pokémon Name: {data['name'].capitalize()}")
    print(f"Base Experience: {data['base_experience']}")
    
def display_pokemon_stats(date):
    print("\nPokémon Details:")
    print(f"Name: {data['name'].capitalize()}")
    print(f"Base Experience: {data['base_experience']}")
    
# display types
types = [t['type']['name'] for t in data['types']]
print(f"Types: {', '.join(types)}")

# display stats
print("\nStats:")
for stat in data['stats']:
    print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
    
# display abilities
print("\nAbilities:")
for ability in data['abilities']:
    print(f"- {ability['ability']['name'].capitalize()}")
    
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