import requests
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta
import time
import sys
import os
import random
import threading
import json

# Ensure UTF-8 encoding is used
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Colorama for colored output
init(autoreset=True, convert=True)

# Define the API key and base URLs
API_KEY = "f5e6221e52b39e2c780520e5f85e7354"  # Replace with your OpenWeatherMap API key
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
AIR_QUALITY_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
ONE_CALL_URL = "http://api.openweathermap.org/data/2.5/onecall"

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
    Simulate faster typing animation for large outputs.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Generate ASCII bar chart
def ascii_bar_chart(values, label, max_width=30):
    """
    Generate an ASCII bar chart for a list of values.
    """
    max_value = max(values)
    scale = max_width / max_value if max_value > 0 else 0
    chart = []
    for value in values:
        bar = "#" * int(value * scale)
        chart.append(f"{label}: {value}°F | {bar}")
    return "\n".join(chart)

# Fun facts generator
def weather_fun_fact():
    """
    Provide a random weather-related fun fact.
    """
    facts = [
        "Did you know? The highest temperature ever recorded on Earth was 134°F in Furnace Creek, California, in 1913!",
        "Rainbows are actually full circles, but we usually see only the top half from the ground.",
        "Lightning can be up to five times hotter than the surface of the sun!",
        "The fastest wind speed ever recorded was 253 mph during a tropical cyclone in Australia in 1996.",
    ]
    return random.choice(facts)

# Real-Time Weather Updates
def real_time_updates(city, interval=300, updates=10):
    """
    Provide real-time weather updates for the specified city.
    Updates every 'interval' seconds, up to 'updates' number of times.
    """
    type_out(Fore.GREEN + f"\nStarting real-time updates for {city}. Updates every {interval // 60} minutes.")
    type_out(Fore.RED + "Press Ctrl+C to stop." + Style.RESET_ALL)
    try:
        for _ in range(updates):  # Limit updates
            weather_data = get_weather(city)
            if weather_data:
                display_weather(weather_data)
            time.sleep(interval)
    except KeyboardInterrupt:
        type_out(Fore.RED + "\nReal-time updates stopped." + Style.RESET_ALL)

# Retro ASCII art introduction
def show_intro():
    """
    Display a retro-style welcome screen with ASCII art.
    """
    type_out(Fore.GREEN + Back.BLACK + """
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
    """ + Style.RESET_ALL, delay=0.001)

    type_out(Fore.CYAN + "Welcome to the Weather Application!" + Style.RESET_ALL)

# Loading animation
def loading_effect():
    """
    Simulate a loading animation.
    """
    type_out(Fore.YELLOW + "Fetching data", delay=0.004)
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
    """
    Display 5-day weather forecast in a formatted layout.
    """
    type_out(Fore.CYAN + "\n5-Day Weather Forecast:")
    type_out(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    # Group forecast data by day
    forecast_by_day = {}
    for forecast in data["list"]:
        timestamp = datetime.fromtimestamp(forecast["dt"])
        date = timestamp.strftime("%A, %b %d")
        time = timestamp.strftime("%I:%M %p")
        temp = forecast["main"]["temp"]
        weather_desc = forecast["weather"][0]["description"].capitalize()
        if date not in forecast_by_day:
            forecast_by_day[date] = []
        forecast_by_day[date].append((time, temp, weather_desc))
    
    # Print grouped forecast
    for date, forecasts in forecast_by_day.items():
        type_out(Fore.LIGHTGREEN_EX + f"\n{date}" + Style.RESET_ALL)
        type_out(Fore.LIGHTGREEN_EX + "-" * 30 + Style.RESET_ALL)
        for time, temp, weather_desc in forecasts:
            type_out_fast(Fore.YELLOW + f"{time}: {temp}°F, {weather_desc}" + Style.RESET_ALL)
        type_out(Fore.LIGHTGREEN_EX + "-" * 30 + Style.RESET_ALL)

# Fetch user's current location
def get_location():
    """
    Detect user's current location using IP-based geolocation.
    """
    try:
        response = requests.get("https://ipinfo.io/json")
        location_data = response.json()
        return location_data.get("city", "Unknown Location")
    except Exception as e:
        type_out(Fore.RED + f"Unable to fetch location. Error: {e}")
        return "Unknown Location"

# Loading animation
def loading_effect():
    """
    Simulate a loading animation.
    """
    type_out(Fore.YELLOW + "Fetching data", delay=0.004)
    for _ in range(3):
        time.sleep(0.5)
        sys.stdout.write(Fore.YELLOW + ".")
        sys.stdout.flush()
    print(Style.RESET_ALL)

# Fun facts generator
def weather_fun_fact():
    """
    Provide a random weather-related fun fact.
    """
    facts = [
        "Did you know? The highest temperature ever recorded on Earth was 134°F in Furnace Creek, California, in 1913!",
        "Rainbows are actually full circles, but we usually see only the top half from the ground.",
        "Lightning can be up to five times hotter than the surface of the sun!",
        "The fastest wind speed ever recorded was 253 mph during a tropical cyclone in Australia in 1996.",
        "The coldest temperature ever recorded on Earth was -128.6°F in Antarctica in 1983!",
    ]
    return random.choice(facts)

# Save preferences
def save_preferences(preferences, filename="preferences.json"):
    """
    Save user preferences to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(preferences, f)
    type_out(Fore.GREEN + "Preferences saved successfully!" + Style.RESET_ALL)

# Load preferences
def load_preferences(filename="preferences.json"):
    """
    Load user preferences from a JSON file.
    """
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    type_out(Fore.YELLOW + "No preferences found. Using defaults." + Style.RESET_ALL)
    return {}

def get_lat_lon(city):
    """
    Retrieve latitude and longitude for the specified city.
    """
    weather_data = get_weather(city)
    if weather_data:
        return weather_data["coord"]["lat"], weather_data["coord"]["lon"]
    return None, None

# Main menu
def main_menu():
    type_out(Fore.GREEN + "\nPlease select an option:")
    type_out(Fore.YELLOW + "1. Today's forecast for your current location")
    type_out(Fore.YELLOW + "2. Enter a city manually")
    type_out(Fore.YELLOW + "3. 5-Day Forecast for your current location")
    type_out(Fore.YELLOW + "4. Show hourly forecast for the next 24 hours.")
    type_out(Fore.YELLOW + "5. Real-time weather updates.")
    type_out(Fore.YELLOW + "6. Exit.")
    
def fetch_hourly_data(lat, lon):
    """
    Fetch hourly weather forecast for the given latitude and longitude.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "imperial",
    }
    try:
        response = requests.get(ONE_CALL_URL, params=params)
        data = response.json()
        if "hourly" in data:
            return data["hourly"]
        else:
            type_out(Fore.RED + "No hourly data available." + Style.RESET_ALL)
            return None
    except Exception as e:
        type_out(Fore.RED + f"An error occurred while fetching hourly data: {e}" + Style.RESET_ALL)
        return None


def main():
    # Show intro and initialize city
    show_intro()
    city = get_location()
    if city == "Unknown Location":
        city = input(Fore.YELLOW + "Unable to detect your location. Please enter a city: " + Style.RESET_ALL)


    while True:
        main_menu()
        choice = input(Fore.CYAN + "\nEnter your choice (1-8): " + Style.RESET_ALL)

        if choice == "1":  # Today's forecast
            type_out(Fore.GREEN + f"\nFetching weather for your current location: {city}" + Style.RESET_ALL)
            loading_effect()
            weather_data = get_weather(city)
            if weather_data:
                display_weather(weather_data)

        elif choice == "2":  # Enter city manually
            city = input(Fore.GREEN + "Enter the name of a city: " + Style.RESET_ALL)
            loading_effect()
            weather_data = get_weather(city)
            if weather_data:
                display_weather(weather_data)

        elif choice == "3":  # 5-Day Forecast
            type_out(Fore.GREEN + f"\nFetching 5-day forecast for your current location: {city}" + Style.RESET_ALL)
            loading_effect()
            forecast_data = get_forecast(city)
            if forecast_data:
                display_forecast(forecast_data)

        elif choice == "4":  # Hourly Forecast
            lat, lon = get_lat_lon(city)  # Fetch latitude and longitude
            if lat and lon:
                hourly_data = fetch_hourly_data(lat, lon)  # Fetch hourly data
                if hourly_data:
                    display_hourly_forecast(hourly_data)
                else:
                    type_out(Fore.RED + "Error fetching hourly data." + Style.RESET_ALL)
            else:
                type_out(Fore.RED + f"Unable to fetch location for {city}." + Style.RESET_ALL)

        elif choice == "5":  # Real-Time Weather Updates
            type_out(Fore.GREEN + "\nHow often would you like updates (in minutes)? Default is 5 minutes." + Style.RESET_ALL)
            try:
                interval = int(input(Fore.CYAN + "Enter the interval in minutes: " + Style.RESET_ALL)) * 60
            except ValueError:
                interval = 300  # Default to 5 minutes if input is invalid
                type_out(Fore.RED + "Invalid input. Using default interval of 5 minutes." + Style.RESET_ALL)
            real_time_updates(city, interval)

        elif choice == "6":  # Save Preferences
            preferences = {"city": city}
            save_preferences(preferences)

        elif choice == "7":  # Load Preferences
            preferences = load_preferences()
            city = preferences.get("city", city)
            type_out(Fore.GREEN + f"Preferences loaded! Default city set to {city}" + Style.RESET_ALL)

        elif choice == "8":  # Exit
            type_out(Fore.GREEN + "\nThank you for using the Weather Application! Goodbye!" + Style.RESET_ALL)
            break

        else:
            type_out(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


# Generate ASCII bar chart
def ascii_bar_chart(values, max_width=30):
    """
    Generate an ASCII bar chart for a list of values.
    """
    max_value = max(values)
    scale = max_width / max_value if max_value > 0 else 0
    chart = []
    for idx, value in enumerate(values):
        bar = "█" * int(value * scale)
        chart.append(f"Day {idx + 1}: {value}°F | {bar}")
    return "\n".join(chart)

# Enhanced display_forecast with ASCII chart
def display_forecast(data):
    """
    Display 5-day weather forecast with an ASCII chart.
    """
    type_out(Fore.CYAN + "\n5-Day Weather Forecast:")
    type_out(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    # Group forecast data by day
    forecast_by_day = {}
    temperatures = []
    for forecast in data["list"]:
        timestamp = datetime.fromtimestamp(forecast["dt"])
        date = timestamp.strftime("%A, %b %d")
        temp = forecast["main"]["temp"]
        weather_desc = forecast["weather"][0]["description"].capitalize()
        if date not in forecast_by_day:
            forecast_by_day[date] = []
        forecast_by_day[date].append(temp)
    
    # Average temperatures per day and prepare chart data
    daily_averages = []
    for date, temps in forecast_by_day.items():
        avg_temp = round(sum(temps) / len(temps), 1)
        daily_averages.append(avg_temp)
        temperatures.append(avg_temp)

    # Print grouped forecast with daily averages
    for idx, (date, avg_temp) in enumerate(zip(forecast_by_day.keys(), daily_averages)):
        type_out(Fore.LIGHTGREEN_EX + f"\n{date}" + Style.RESET_ALL)
        type_out(Fore.LIGHTGREEN_EX + "-" * 30 + Style.RESET_ALL)
        type_out(Fore.YELLOW + f"Average Temperature: {avg_temp}°F")
    
    # Display ASCII chart
    type_out(Fore.CYAN + "\nTemperature Trend (5 Days):")
    type_out(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    chart = ascii_bar_chart(temperatures)
    type_out(Fore.LIGHTCYAN_EX + chart + Style.RESET_ALL)

# Fetch hourly weather data
def display_hourly_forecast(hourly_data):
    """
    Display hourly weather forecast for the next 24 hours.
    """
    type_out(Fore.CYAN + "\nHourly Weather Forecast (Next 24 Hours):")
    type_out(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
    
    for hour in hourly_data[:24]:  # Limit to next 24 hours
        timestamp = datetime.fromtimestamp(hour["dt"])
        time_str = timestamp.strftime("%I:%M %p")
        temp = hour["temp"]
        weather_desc = hour["weather"][0]["description"].capitalize()
        type_out_fast(Fore.YELLOW + f"{time_str}: {temp}°F, {weather_desc}")
    
    type_out(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

def main_menu():
    type_out(Fore.GREEN + "\nPlease select an option:")
    type_out(Fore.YELLOW + "1. Today's forecast for your current location")
    type_out(Fore.YELLOW + "2. Enter a city manually")
    type_out(Fore.YELLOW + "3. 5-Day Forecast with ASCII Chart")
    type_out(Fore.YELLOW + "4. Hourly Forecast for Next 24 Hours")
    type_out(Fore.YELLOW + "5. Real-Time Weather Updates")
    type_out(Fore.YELLOW + "6. Save Preferences")
    type_out(Fore.YELLOW + "7. Load Preferences")
    type_out(Fore.YELLOW + "8. Exit")

if __name__ == "__main__":
    main()
