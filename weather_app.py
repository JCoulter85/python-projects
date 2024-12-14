import requests
from colorama import init, Fore, Style
from datetime import datetime
import time
import sys

# Initialize Colorama for colored output
init(autoreset=True, convert=True)

# Define the API key and base URLs
API_KEY = "f5e6221e52b39e2c780520e5f85e7354"  # Replace with your OpenWeatherMap API key
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
AIR_QUALITY_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# Typing animation function
def type_out(text, delay=0.03):
    """
    Simulate retro typing animation.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Faster typing animation for forecast
def type_out_fast(text, delay=0.001):
    """
    Simulate faster retro typing animation for large outputs.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Retro ASCII art introduction
def show_intro():
    """
    Display a retro-style welcome screen with ASCII art.
    """
    type_out(Fore.GREEN + """
                                 ⠀⠀⠀⣀⡠⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠃⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠾⢛⠒⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⣄⡈⠓⢄⠠⡀⠀⠀⠀⣄⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣷⠀⠈⠱⡄⠑⣌⠆⠀⠀⡜⢻⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠳⡆⠐⢿⣆⠈⢿⠀⠀⡇⠘⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣷⡇⠀⠀⠈⢆⠈⠆⢸⠀⠀⢣⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⠀⠀⠈⢂⠀⡇⠀⠀⢨⠓⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣦⣤⠖⡏⡸⠀⣀⡴⠋⠀⠈⠢⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠁⣹⣿⣿⣿⣷⣾⠽⠖⠊⢹⣀⠄⠀⠀⠀⠈⢣⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⣇⣰⢫⢻⢉⠉⠀⣿⡆⠀⠀⡸⡏⠀⠀⠀⠀⠀⠀⢇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡇⡇⠈⢸⢸⢸⠀⠀⡇⡇⠀⠀⠁⠻⡄⡠⠂⠀⠀⠀⠘
⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠓⡇⠀⠸⡆⢸⠀⢠⣿⠀⠀⠀⠀⣰⣿⣵⡆⠀⠀⠀⠀
⠈⢻⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⣦⣀⡇⠀⢧⡇⠀⠀⢺⡟⠀⠀⠀⢰⠉⣰⠟⠊⣠⠂⠀⡸
⠀⠀⢻⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢧⡙⠺⠿⡇⠀⠘⠇⠀⠀⢸⣧⠀⠀⢠⠃⣾⣌⠉⠩⠭⠍⣉⡇
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣞⣋⠀⠈⠀⡳⣧⠀⠀⠀⠀⠀⢸⡏⠀⠀⡞⢰⠉⠉⠉⠉⠉⠓⢻⠃
⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⢀⣀⠠⠤⣤⣤⠤⠞⠓⢠⠈⡆⠀⢣⣸⣾⠆⠀⠀⠀⠀⠀⢀⣀⡼⠁⡿⠈⣉⣉⣒⡒⠢⡼⠀
⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣎⣽⣶⣤⡶⢋⣤⠃⣠⡦⢀⡼⢦⣾⡤⠚⣟⣁⣀⣀⣀⣀⠀⣀⣈⣀⣠⣾⣅⠀⠑⠂⠤⠌⣩⡇⠀
⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣺⢁⣞⣉⡴⠟⡀⠀⠀⠀⠁⠸⡅⠀⠈⢷⠈⠏⠙⠀⢹⡛⠀⢉⠀⠀⠀⣀⣀⣼⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡟⢡⠖⣡⡴⠂⣀⣀⣀⣰⣁⣀⣀⣸⠀⠀⠀⠀⠈⠁⠀⠀⠈⠀⣠⠜⠋⣠⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⢿⣿⣿⣷⡟⢋⣥⣖⣉⠀⠈⢁⡀⠤⠚⠿⣷⡦⢀⣠⣀⠢⣄⣀⡠⠔⠋⠁⠀⣼⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡄⠈⠻⣿⣿⢿⣛⣩⠤⠒⠉⠁⠀⠀⠀⠀⠀⠉⠒⢤⡀⠉⠁⠀⠀⠀⠀⠀⢀⡿⠀⠀⠀
    """ + Style.RESET_ALL, delay=0.01)
    
    type_out(Fore.CYAN + "Welcome to the Weather Application!" + Style.RESET_ALL)

# Loading animation
def loading_effect():
    """
    Simulate a loading animation.
    """
    type_out(Fore.YELLOW + "Fetching data", delay=0.05)
    for _ in range(3):
        time.sleep(0.5)
        sys.stdout.write(Fore.YELLOW + ".")
        sys.stdout.flush()
    print(Style.RESET_ALL)

# Fetch current weather data
def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"
    }
    try:
        response = requests.get(CURRENT_WEATHER_URL, params=params)
        data = response.json()
        if data["cod"] != 200:
            type_out(Fore.RED + f"Error: {data['message']}")
            return None
        return data
    except Exception as e:
        type_out(Fore.RED + f"An error occurred: {e}")
        return None

# Fetch 5-day forecast data
def get_forecast(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"
    }
    try:
        response = requests.get(FORECAST_URL, params=params)
        data = response.json()
        if data["cod"] != "200":
            type_out(Fore.RED + f"Error: {data['message']}")
            return None
        return data
    except Exception as e:
        type_out(Fore.RED + f"An error occurred: {e}")
        return None

# Fetch air quality data
def get_air_quality(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }
    try:
        response = requests.get(AIR_QUALITY_URL, params=params)
        data = response.json()
        return data["list"][0] if "list" in data else None
    except Exception as e:
        type_out(Fore.RED + f"An error occurred while fetching air quality data: {e}")
        return None

# Display current weather in a retro dashboard-style layout
def display_weather(data):
    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    weather_desc = data["weather"][0]["description"].capitalize()
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
    lat, lon = data["coord"]["lat"], data["coord"]["lon"]

    air_quality = get_air_quality(lat, lon)
    aqi = air_quality["main"]["aqi"] if air_quality else "N/A"
    air_desc = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
    air_status = air_desc[aqi - 1] if air_quality and 1 <= aqi <= 5 else "Unknown"

    type_out(Fore.LIGHTCYAN_EX + "\n==============================")
    type_out(Fore.LIGHTCYAN_EX + f"  {city.upper()} WEATHER  ")
    type_out(Fore.LIGHTCYAN_EX + "==============================")
    type_out(Fore.GREEN + f"  Temperature: {temp}°F")
    type_out(Fore.GREEN + f"  Condition: {weather_desc}")
    type_out(Fore.GREEN + f"  Humidity: {humidity}%")
    type_out(Fore.GREEN + f"  Wind Speed: {wind_speed} mph")
    type_out(Fore.GREEN + f"  Sunrise: {sunrise}")
    type_out(Fore.GREEN + f"  Sunset: {sunset}")
    type_out(Fore.YELLOW + f"  Air Quality Index: {aqi} ({air_status})")
    type_out(Fore.LIGHTCYAN_EX + "==============================\n" + Style.RESET_ALL)

# Display 5-day forecast in a retro layout
def display_forecast(data):
    type_out(Fore.CYAN + "\n5-Day Weather Forecast:")
    type_out(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    for forecast in data["list"]:
        timestamp = datetime.fromtimestamp(forecast["dt"])
        date_time = timestamp.strftime("%A, %b %d %I:%M %p")
        temp = forecast["main"]["temp"]
        weather_desc = forecast["weather"][0]["description"].capitalize()
        type_out_fast(Fore.GREEN + f"{date_time}")
        type_out_fast(Fore.YELLOW + f"  Temperature: {temp}°F")
        type_out_fast(Fore.MAGENTA + f"  Condition: {weather_desc}")
        type_out_fast(Style.RESET_ALL + "-" * 40)

# Fetch user's current location
def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        location_data = response.json()
        return location_data.get("city", "Unknown Location")
    except Exception as e:
        type_out(Fore.RED + f"Unable to fetch location. Error: {e}")
        return "Unknown Location"

# Main menu
def main_menu():
    type_out(Fore.GREEN + "\nPlease select an option:")
    type_out(Fore.YELLOW + "1. Today's forecast for your current location")
    type_out(Fore.YELLOW + "2. Enter a city manually")
    type_out(Fore.YELLOW + "3. 5-Day Forecast for your current location")
    type_out(Fore.YELLOW + "4. Exit")

# Main application logic
def main():
    show_intro()
    city = get_location()
    while True:
        main_menu()
        choice = input(Fore.CYAN + "\nEnter your choice (1/2/3/4): " + Style.RESET_ALL)
        if choice == "1":
            type_out(Fore.GREEN + f"\nFetching weather for your current location: {city}" + Style.RESET_ALL)
            loading_effect()
            weather_data = get_weather(city)
            if weather_data:
                display_weather(weather_data)
        elif choice == "2":
            city = input(Fore.GREEN + "Enter the name of a city: " + Style.RESET_ALL)
            loading_effect()
            weather_data = get_weather(city)
            if weather_data:
                display_weather(weather_data)
        elif choice == "3":
            type_out(Fore.GREEN + f"\nFetching 5-day forecast for your current location: {city}" + Style.RESET_ALL)
            loading_effect()
            forecast_data = get_forecast(city)
            if forecast_data:
                display_forecast(forecast_data)
        elif choice == "4":
            type_out(Fore.GREEN + "\nThank you for using the Weather Application! Goodbye!" + Style.RESET_ALL)
            break
        else:
            type_out(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
