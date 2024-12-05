import requests

# Fetch Pokémon data from the API
def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Pokémon not found! Please check the name.")
        return None

# Fetch evolution chain from species data
def get_evolution_chain(species_url):
    response = requests.get(species_url)
    if response.status_code == 200:
        species_data = response.json()
        evolution_chain_url = species_data['evolution_chain']['url']
        evolution_response = requests.get(evolution_chain_url)
        
        if evolution_response.status_code == 200:
            evolution_data = evolution_response.json()
            chain = evolution_data['chain']
            
            evolutions = []
            while chain:
                evolutions.append(chain['species']['name'].capitalize())
                chain = chain['evolves_to'][0] if chain['evolves_to'] else None
            return evolutions
    return []

# Fetch weaknesses based on Pokémon types
def get_weaknesses(types):
    weaknesses = set()
    for pokemon_type in types:
        type_url = pokemon_type['type']['url']
        response = requests.get(type_url)
        
        if response.status_code == 200:
            type_data = response.json()
            for weak_type in type_data['damage_relations']['double_damage_from']:
                weaknesses.add(weak_type['name'])
    return list(weaknesses)

# Display Pokémon stats
def display_pokemon_stats(data):
    print("\nPokémon Details:")
    print(f"Name: {data['name'].capitalize()}")
    print(f"Base Experience: {data['base_experience']}")
    
    # Extract and display types
    types = data.get('types', [])
    if not types:
        print("No types found for this Pokémon.")
        return

    type_names = [t['type']['name'] for t in types]
    print(f"Types: {', '.join(type_names)}")
    
    # Display stats
    print("\nStats:")
    for stat in data['stats']:
        print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
    
    # Display abilities
    print("\nAbilities:")
    for ability in data['abilities']:
        print(f"- {ability['ability']['name'].capitalize()}")
    
      
    # Display moves specific to the Pokémon
    print("\nMoves (Specific to This Pokémon):")
    level_up_moves = [
        move['move']['name'].capitalize()
        for move in data['moves']
        if any(method['move_learn_method']['name'] == 'level-up' for method in move['version_group_details'])
    ]
    if level_up_moves:
        print(", ".join(level_up_moves[:10]))  # Limit to 10 moves
    else:
        print("No level-up moves found for this Pokémon.")
    
    # Fetch and display evolution chain
    print("\nEvolution Chain:")
    species_url = data['species']['url']
    evolutions = get_evolution_chain(species_url)
    print(" → ".join(evolutions))

     # Fetch and display weaknesses
    weaknesses = get_weaknesses(types)
    print("\nWeaknesses:")
    print(", ".join(weaknesses))

# Main loop
while True:
    pokemon_name = input("\nEnter Pokémon name (or type 'quit' to exit): ").strip()
    
    if pokemon_name.lower() == "quit":
        print("Goodbye!")
        break

    data = get_pokemon_data(pokemon_name)
    if not data:
        print("No data available for this Pokémon.")
        continue

    display_pokemon_stats(data)
