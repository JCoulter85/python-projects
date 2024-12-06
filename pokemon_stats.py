import requests
from tkinter import Tk, Label
from PIL import Image, ImageTk
import io
from colorama import Fore, Style, init

# Initialize colorama with conversion for Windows CMD
init(convert=True)

# Fetch Pokémon data from the API
def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.RED + "Pokémon not found! Please check the name." + Style.RESET_ALL)
        return None

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

# Display Pokémon image using tkinter
def show_pokemon_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((200, 200))

        # Display image in a tkinter window
        root = Tk()
        root.title("Pokémon Image")
        img = ImageTk.PhotoImage(image)
        label = Label(root, image=img)
        label.image = img
        label.pack()
        root.mainloop()

# Display Pokémon stats
def display_pokemon_stats(data):
    print(Fore.YELLOW + "\nPokémon Details:" + Style.RESET_ALL)
    print(Fore.GREEN + f"Name: {data['name'].capitalize()}" + Style.RESET_ALL)
    print(f"Base Experience: {data['base_experience']}")
    
    # Extract and display types
    types = data.get('types', [])
    if not types:
        print("No types found for this Pokémon.")
        return

    type_names = [t['type']['name'] for t in types]
    print(Fore.CYAN + f"Types: {', '.join(type_names)}" + Style.RESET_ALL)
    
    # Display stats
    print(Fore.BLUE + "\nStats:" + Style.RESET_ALL)
    for stat in data['stats']:
        print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
    
    # Display abilities
    print(Fore.MAGENTA + "\nAbilities:" + Style.RESET_ALL)
    for ability in data['abilities']:
        print(f"- {ability['ability']['name'].capitalize()}")
    
    # Display Pokémon moves
    print(Fore.YELLOW + "\nMoves (Specific to This Pokémon):" + Style.RESET_ALL)
    level_up_moves = [
        move['move']['name'].capitalize()
        for move in data['moves']
        if any(method['move_learn_method']['name'] == 'level-up' for method in move['version_group_details'])
    ]
    if level_up_moves:
        print(", ".join(level_up_moves[:10]))  # Limit to 10 moves
    else:
        print("No level-up moves found for this Pokémon.")

    # Fetch and display weaknesses
    weaknesses = get_weaknesses(types)
    print(Fore.RED + "\nWeaknesses:" + Style.RESET_ALL)
    print(", ".join(weaknesses))
    
    # Fetch and display evolution chain
    print(Fore.YELLOW + "\nEvolution Chain:" + Style.RESET_ALL)
    species_url = data['species']['url']
    evolutions = get_evolution_chain(species_url)
    print(" → ".join(evolutions))

    # Show Pokémon sprite
    sprite_url = data['sprites']['front_default']
    if sprite_url:
        print("\nDisplaying Pokémon image...")
        show_pokemon_image(sprite_url)
    else:
        print("No image available for this Pokémon.")

# Main loop
while True:
    print(Fore.CYAN + "\nWelcome to the Pokémon Info App!" + Style.RESET_ALL)
    pokemon_name = input(Fore.GREEN + "Enter Pokémon name (or type 'quit' to exit): " + Style.RESET_ALL).strip()
    
    if pokemon_name.lower() == "quit":
        print(Fore.RED + "Goodbye!" + Style.RESET_ALL)
        break

    data = get_pokemon_data(pokemon_name)
    if not data:
        print(Fore.RED + "No data available for this Pokémon." + Style.RESET_ALL)
        continue

    display_pokemon_stats(data)
