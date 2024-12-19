import requests
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta
import time
import sys
import os
import random
import json
from pytz import timezone

# Ensure UTF-8 encoding is used
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Colorama for colored output
init(autoreset=True, convert=True)

# Define the API key and base URLs
API_KEY = os.getenv("f5e6221e52b39e2c780520e5f85e7354")
if not API_KEY:
    raise ValueError("API Key not found. Set the OPENWEATHER_API_KEY environment variable.")
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
def ascii_bar_chart(values, label="Temperature", max_width=30):
    """
    Generate an ASCII bar chart for a list of values.
    """
    max_value = max(values)
    scale = max_width / max_value if max_value > 0 else 0
    chart = []
    for value in values:
        bar = "█" * int(value * scale)
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
        "The coldest temperature ever recorded on Earth was -128.6°F in Antarctica in 1983!",
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
                                ⁠⁠⁠⁠
    """ + Style.RESET_ALL, delay=0.001)

    type_out(Fore.CYAN + "Welcome to the Weather Application!" + Style.RESET_ALL)

# Fetch current weather data
def get_weather(city):
    """
    Fetch current weather data for the specified city.
    """
    params = {"q": city, "appid": API_KEY, "units": "imperial"}
    try:
        response = requests.get(CURRENT_WEATHER_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("cod") != 200:
            type_out(Fore.RED + f"Error: {data.get('message', 'Unknown error')}")
            return None
        return data
    except requests.exceptions.RequestException as e:
        type_out(Fore.RED + f"An error occurred while fetching weather data: {e}")
        return None

# Display current weather in a retro dashboard-style layout
def display_weather(data):
    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    weather_desc = data["weather"][0]["description"].capitalize()
    lat, lon = data["coord"]["lat"], data["coord"]["lon"]

    # Convert sunrise/sunset to local time
    tz_offset = data["timezone"]  # Offset in seconds
    local_time = datetime.now() + timedelta(seconds=tz_offset)
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]) + timedelta(seconds=tz_offset)
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]) + timedelta(seconds=tz_offset)

    type_out(Fore.LIGHTCYAN_EX + "\n==============================")
    type_out(Fore.LIGHTCYAN_EX + f"  {city.upper()} WEATHER  ")
    type_out(Fore.LIGHTCYAN_EX + "==============================")
    type_out(Fore.GREEN + f"  Local Time: {local_time.strftime('%I:%M %p')}")
    type_out(Fore.GREEN + f"  Temperature: {temp}°F")
    type_out(Fore.GREEN + f"  Condition: {weather_desc}")
    type_out(Fore.GREEN + f"  Humidity: {humidity}%")
    type_out(Fore.GREEN + f"  Wind Speed: {wind_speed} mph")
    type_out(Fore.GREEN + f"  Sunrise: {sunrise.strftime('%I:%M %p')}")
    type_out(Fore.GREEN + f"  Sunset: {sunset.strftime('%I:%M %p')}")
    type_out(Fore.LIGHTCYAN_EX + "==============================\n" + Style.RESET_ALL)

# Display 5-Day Forecast with ASCII Chart
def display_forecast(data):
    """
    Display 5-day weather forecast in a formatted layout.
    """
    type_out(Fore.CYAN + "\n5-Day Weather Forecast:")
    type_out(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    forecast_by_day = {}
    for forecast in data["list"]:
        timestamp = datetime.fromtimestamp(forecast["dt"])
        date = timestamp.strftime("%A, %b %d")
        temp = forecast["main"]["temp"]
        weather_desc = forecast["weather"][0]["description"].capitalize()
        if date not in forecast_by_day:
            forecast_by_day[date] = []
        forecast_by_day[date].append(temp)

    # Calculate and display daily averages
    for date, temps in forecast_by_day.items():
        avg_temp = round(sum(temps) / len(temps), 1)
        type_out(Fore.LIGHTGREEN_EX + f"\n{date}: {avg_temp}°F")
        chart = ascii_bar_chart(temps, label="Daily Temperatures")
        type_out(Fore.LIGHTCYAN_EX + chart + Style.RESET_ALL)

if __name__ == "__main__":
    show_intro()
    city = input(Fore.YELLOW + "Enter your city: " + Style.RESET_ALL)
    weather_data = get_weather(city)
    if weather_data:
        display_weather(weather_data)
    forecast_data = requests.get(FORECAST_URL, params={"q": city, "appid": API_KEY, "units": "imperial"}).json()
    if forecast_data:
        display_forecast(forecast_data)