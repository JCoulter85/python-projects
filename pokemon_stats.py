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