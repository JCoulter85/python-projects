import requests
from colorama import init, Fore, Back, Style
from datetime import datetime, timedelta, timezone  # Add timezone here
import time
import sys
import os
import random
import json

# Ensure UTF-8 encoding is used
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Colorama for colored output
init(autoreset=True, convert=True)

# Define the API key and base URLs
API_KEY = os.getenv("OPENWEATHER_API_KEY", "f5e6221e52b39e2c780520e5f85e7354")  # Replace with your actual API key
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
AIR_QUALITY_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
ONE_CALL_URL = "http://api.openweathermap.org/data/2.5/onecall"

# Typing animation function with green text on black background
def type_out(text, delay=0.001):
    """
    Simulate retro typing animation with Matrix-style green text on black background.
    """
    for char in text:
        sys.stdout.write(Fore.LIGHTGREEN_EX + Back.BLACK + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

# ASCII art for menu options
def display_ascii(option):
    art = {
        "1": """
░█░█░█▀▀░█▀▀░█▀▄░░░█▀▀░█░█░█▀▄░█▀▄░█▀▀░█▀█░▀█▀
░█░█░▀▀█░█▀▀░█▀▄░░░█░░░█░█░█▀▄░█▀▄░█▀▀░█░█░░█░
░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀░░▀░
░█░░░█▀█░█▀▀░█▀█░▀█▀░▀█▀░█▀█░█▀█              
░█░░░█░█░█░░░█▀█░░█░░░█░░█░█░█░█              
░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀░▀               
        """,
        "2": """
░█▀▀░█▀▀░█░░░█▀▀░█▀▀░▀█▀░░░█▀█░░░█▀▀░▀█▀░▀█▀░█░█
░▀▀█░█▀▀░█░░░█▀▀░█░░░░█░░░░█▀█░░░█░░░░█░░░█░░░█░
░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░░░░▀░▀░░░▀▀▀░▀▀▀░░▀░░░▀░
░█▄█░█▀█░█▀█░█░█░█▀█░█░░░█░░░█░█                
░█░█░█▀█░█░█░█░█░█▀█░█░░░█░░░░█░                
░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░                
        """,
        "3": """
░█░█░▀█▀░█▀▀░█░█░░░▀█▀░█▀█░█▀▄░█▀█░█░█░▀░█▀▀░░░█░█░█▀▀░█▀█░▀█▀░█░█░█▀▀░█▀▄
░▀▄▀░░█░░█▀▀░█▄█░░░░█░░█░█░█░█░█▀█░░█░░░░▀▀█░░░█▄█░█▀▀░█▀█░░█░░█▀█░█▀▀░█▀▄
░░▀░░▀▀▀░▀▀▀░▀░▀░░░░▀░░▀▀▀░▀▀░░▀░▀░░▀░░░░▀▀▀░░░▀░▀░▀▀▀░▀░▀░░▀░░▀░▀░▀▀▀░▀░▀
        """,
        "4": """
░█░█░▀█▀░█▀▀░█░█░░░█▀▀░░░░░█▀▄░█▀█░█░█░░░█▀▀░█▀█░█▀▄░█▀▀░█▀▀░█▀█░█▀▀░▀█▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
░▀▄▀░░█░░█▀▀░█▄█░░░▀▀▄░▄▄▄░█░█░█▀█░░█░░░░█▀▀░█░█░█▀▄░█▀▀░█░░░█▀█░▀▀█░░█░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
░░▀░░▀▀▀░▀▀▀░▀░▀░░░▀▀░░░░░░▀▀░░▀░▀░░▀░░░░▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░▀░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                                                                                  
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██████████▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██         ░▒███▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█      ░ ░░      ░▒██▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓       ░░░░░░░░░░░   ░▒▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█ ░░    ░░░░░░░░░░░░░░░  ░▓▓▓▒▒▒▓▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█  ▒░░░░░   ░░░░░░▒▒▒▒▒▒▒▒░▒█████ ▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█   ▒▓  ▒░░░░ ░░░                ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██    █▓  ░▒░░░░▒▒▒▒▒▒▒▓▓▒▓█▒    ▒██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█     ██▓  ▒▒▒░░░░░░▒░░░░▓▒ █     ░░▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██      ██▓  ░░▒░░░░░░▒▒▒▓ ▓ █████ ▓░░▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█▓       ██▓░  ▒▒▒▒▒░▒▒▓█ ▓▓░░░░▒  ▓░░░▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██        ███▒▒   ░░▒░░ █ █▒▒░░▒▓░░▒░░░░▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██   ░     ███▓▓▒░  ▓▒   █▒▒▒▒░░░ ░▒░░░░░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██          ▓██░▒▓▓▓     ██▒░░▒▒▒ ░░░░░░░▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██  ▒         ███▓  ▓     ▒▓▒░░▒░ ▒▒░░░░ ░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██░             ▓ █ █████  ▒▓▒▒░░ ░░░░░░░ ▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓███              ▒███▒░▒▓▒▒  ▒▒▒░░░░░░░░░░▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓██                   ████▒▒▒▒   ▓▓▒░░░░░░░ ▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ▒                        ░███▓▒▒░   ░░░░░░░ ░▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓░▓░░     ██                    ██████▓░░░░▒▒░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░ █                                  ▒▓     █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓██▒              ▓██                █   ▒████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓███░              ███████████▓████████████▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ░▒▒▓██░         ██▒▒▒▒▒▒▒▓▓█████▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█▒  █    ▓        █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒     ██▒████▓    █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█   ░             █▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓█   █             ██▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██  ▓   ░           ▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██     ░▒▒▓▒▓▒▒░  █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█ ▓ ▓▒░▒▒▓▒▒▒▒▓▒ ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█                 █▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                                             
            """,
        "5": """
░█▀▀░█░█░█▀█░░░█▀▀░█▀█░█▀▀░▀█▀░█▀▀
░█▀▀░█░█░█░█░░░█▀▀░█▀█░█░░░░█░░▀▀█
░▀░░░▀▀▀░▀░▀░░░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀
            """,
        "6": """
░█▀▀░█▀█░█▀█░█▀▄░█▀▄░█░█░█▀▀░█░█░░░█▀▀░▀█▀░█▀█░█░█░░░█▀▀░█▀█░█▀▀░█▀▀░█░█
░█░█░█░█░█░█░█░█░█▀▄░░█░░█▀▀░▀░▀░░░▀▀█░░█░░█▀█░░█░░░░▀▀█░█▀█░█▀▀░█▀▀░▀░▀
░▀▀▀░▀▀▀░▀▀▀░▀▀░░▀▀░░░▀░░▀▀▀░▀░▀░░░▀▀▀░░▀░░▀░▀░░▀░░░░▀▀▀░▀░▀░▀░░░▀▀▀░▀░▀
        """
    }
    if option in art:
        type_out(Fore.LIGHTGREEN_EX + art[option] + Style.RESET_ALL, delay=0.0005)

# ASCII bar chart generator
def ascii_bar_chart(values, label="Temperature", max_width=40):
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

# Display ASCII art introduction
def show_intro():
    """
    Display a retro-style welcome screen with ASCII art.
    """
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + """
==========================================================
    ███╗   ███╗ █████╗ ███████╗███████╗███████╗
    ████╗ ████║██╔══██╗╚══███╔╝██╔════╝██╔════╝
    ██╔████╔██║███████║  ███╔╝ █████╗  █████╗  
    ██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ██╔══╝  
    ██║ ╚═╝ ██║██║  ██║███████╗███████╗███████╗
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⡴⠶⠞⠛⠛⠉⠉⠉⠉⠉⠉⠛⠛⠶⢦⣄⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣶⣾⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠈⠛⢦⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⢛⣩⠶⠛⠉⠀⠀⠀⣀⣤⡴⠶⠚⠛⠛⠛⠉⠛⠛⠛⢶⡟⠉⢻⡄⠀⠀⠀⠈⢻⡄
⠀⠀⠀⠀⠀⠀⠀⣠⡴⠟⢉⣠⠶⠋⠁⠀⠀⣠⡴⠞⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠷⡤⠾⣇⠀⠀⠀⠀⠀⣿
⠀⠀⠀⠀⣠⡴⠛⠁⣀⡴⠛⠁⠀⢀⣠⠶⠛⠁⠀⠀⠀⣀⣠⡤⠶⠒⠛⠛⠛⠛⠛⠶⣤⡀⠀⠀⠀⢹⡆⠀⠀⠀⠀⢸
⠀⢀⣴⠟⠁⠀⣠⡾⠋⠀⠀⢀⡴⠛⠁⠀⢰⠞⠳⡶⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⢈⡇⠀⠀⠀⠀⣾
⢴⠟⠁⠀⢀⡼⠋⠀⠀⢀⡴⠋⠀⠀⠀⣠⡾⠷⠶⠇⢀⣠⣤⠶⠖⠲⢶⣄⠀⠀⠀⠀⠀⡿⠀⠀⠀⢸⡇⠀⠀⠀⢰⡏
⠀⠀⠀⣰⠟⠀⠀⠀⣴⠏⠀⠀⠀⣠⠞⠉⠀⠀⣠⡶⠋⠁⠀⠀⠀⠀⢀⡿⠀⠀⠀⠀⣼⠃⠀⠀⢀⡟⠂⠀⠀⢠⡟⠀
⠀⢀⣼⠋⠀⠀⢀⡾⠁⠀⠀⢠⡞⠁⠀⠀⢠⡾⠁⠀⠀⠀⠀⣀⣀⣠⡾⠁⠀⠀⣠⡾⠁⠀⠀⢠⡞⠁⠀⠀⣰⠟⠀⠀
⠀⣾⠃⠀⢠⡟⠛⣷⠂⠀⢠⡟⠀⠀⠀⠀⢾⡀⠀⠀⠀⠀⣸⣏⣹⡏⠀⠀⣠⡾⠋⠀⠀⢀⣴⠏⠀⠀⢀⡼⠋⠀⠀⠀
⣸⠇⠀⠀⠈⢻⡶⠛⠀⠀⣿⠀⠀⠀⠀⠀⠈⠛⠲⠖⠚⠋⠉⠉⠉⣀⣤⠞⠋⠀⠀⢀⣴⠟⠁⠀⠀⣰⠟⠁⠀⣴⠆⠀
⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⠛⠉⣀⣀⡀⣀⡴⠟⠁⠀⢀⣤⠞⠁⢀⣴⠟⠁⠀⠀
⣿⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠙⠳⠶⠤⣤⠤⠶⠶⠚⠋⠉⠀⠀⠀⡟⠉⠈⢻⡏⠀⠀⣀⡴⠛⠁⣠⡶⠋⠁⠀⠀⠀⠀
⢻⡀⠀⠀⠀⠀⠘⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⠶⠻⢦⣤⠟⣀⣤⠞⢋⣠⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠈⢿⣄⠀⠀⠀⠀⠀⠈⠛⠳⠶⠤⠤⠤⠤⠤⠴⠶⠒⠛⠉⠁⠀⠀⢀⣠⡴⣞⣋⣤⠶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⢷⡶⠛⠳⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣾⠿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⣧⡀⣀⣿⠦⣤⣤⣤⣤⣤⣤⠤⠶⠶⠞⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠉⠉
==========================================================
    """ + Style.RESET_ALL, delay=0.001)

# Fetch user's current location
def get_location():
    """
    Detect user's current location using IP-based geolocation.
    """
    try:
        response = requests.get("https://ipinfo.io/json")
        location_data = response.json()
        city = location_data.get("city", "Unknown City")
        region = location_data.get("region", "Unknown State")  # Fetch the state/region
        return city, region
    except Exception as e:
        type_out(Fore.RED + f"Unable to fetch location. Error: {e}")
        return "Unknown City", "Unknown State"

# Option 1: Use current location
def option_one():
    """
    Fetch and display weather information for the user's current location.
    """
    global city
    display_ascii("1")
    city, state = get_location()
    if city == "Unknown City":
        type_out(Fore.RED + "Unable to detect your location. Please try again or select a city manually.")
        return

    type_out(Fore.LIGHTGREEN_EX + f"\nYour current location has been detected as: {city}, {state}")
    weather_data = get_weather(city)
    if weather_data:
        type_out(Fore.LIGHTGREEN_EX + f"\nWeather Information for {city}, {state}:")
        display_weather(weather_data)
    else:
        type_out(Fore.RED + "Unable to fetch weather information for your location.")

# Option 2: Select a city manually
def option_two():
    """
    Allow user to manually enter a city and display weather information.
    """
    global city
    display_ascii("2")
    type_out(Fore.LIGHTGREEN_EX + "\nPlease enter the city and state in the format: City, State")
    user_input = input(Fore.LIGHTGREEN_EX + "City, State: " + Style.RESET_ALL)
    try:
        city, state = map(str.strip, user_input.split(","))
        weather_data = get_weather(city)
        if weather_data:
            type_out(Fore.LIGHTGREEN_EX + f"\nWeather Information for {city}, {state}:")
            display_weather(weather_data)
        else:
            type_out(Fore.RED + "Unable to fetch weather information for the entered city.")
    except ValueError:
        type_out(Fore.RED + "Invalid format. Please use the format: City, State")

# Fetch current weather data
def get_weather(city):
    """
    Fetch current weather data for the specified city.
    """
    params = {"q": city, "appid": API_KEY, "units": "imperial"}
    try:
        response = requests.get(CURRENT_WEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        type_out(Fore.RED + f"Error fetching weather data: {e}")
        return None

# Display current weather
def display_weather(data):
    """
    Display the current weather in a retro dashboard-style layout.
    """
    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    weather_desc = data["weather"][0]["description"].capitalize()

    # Convert sunrise/sunset to local time
    tz_offset = data["timezone"]
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], timezone.utc) + timedelta(seconds=tz_offset)
    sunset = datetime.fromtimestamp(data["sys"]["sunset"], timezone.utc) + timedelta(seconds=tz_offset)

    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Sunrise: {sunrise.strftime('%I:%M %p')}")
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Sunset: {sunset.strftime('%I:%M %p')}")

    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"\n{city.upper()} WEATHER:")
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Temperature: {temp}°F")
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Condition: {weather_desc}")
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Humidity: {humidity}%")
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Wind Speed: {wind_speed} mph")
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Sunrise: {sunrise.strftime('%I:%M %p')}")
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + f"Sunset: {sunset.strftime('%I:%M %p')}")

# Display detailed 5-day forecast
def display_forecast(forecast_data):
    """
    Display a detailed 5-day weather forecast.
    """
    display_ascii("4")
    type_out(Fore.LIGHTGREEN_EX + "\n5-Day Detailed Weather Forecast:")
    type_out(Fore.LIGHTGREEN_EX + "-" * 50)

    forecast_by_day = {}
    for entry in forecast_data["list"]:
        dt = datetime.fromtimestamp(entry["dt"])
        date = dt.strftime("%A, %b %d")
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        wind_speed = entry["wind"]["speed"]
        condition = entry["weather"][0]["description"].capitalize()

        if date not in forecast_by_day:
            forecast_by_day[date] = {
                "temps": [],
                "humidities": [],
                "wind_speeds": [],
                "conditions": [],
            }

        forecast_by_day[date]["temps"].append(temp)
        forecast_by_day[date]["humidities"].append(humidity)
        forecast_by_day[date]["wind_speeds"].append(wind_speed)
        forecast_by_day[date]["conditions"].append(condition)

    # Display detailed forecast for each day
    for date, details in forecast_by_day.items():
        avg_temp = round(sum(details["temps"]) / len(details["temps"]), 1)
        high_temp = round(max(details["temps"]), 1)
        low_temp = round(min(details["temps"]), 1)
        avg_humidity = round(sum(details["humidities"]) / len(details["humidities"]), 1)
        avg_wind_speed = round(sum(details["wind_speeds"]) / len(details["wind_speeds"]), 1)
        most_common_condition = max(set(details["conditions"]), key=details["conditions"].count)

        type_out(Fore.LIGHTGREEN_EX + f"\n{date}")
        type_out(Fore.LIGHTGREEN_EX + f"  High: {high_temp}°F | Low: {low_temp}°F | Avg: {avg_temp}°F")
        type_out(Fore.LIGHTGREEN_EX + f"  Avg Humidity: {avg_humidity}%")
        type_out(Fore.LIGHTGREEN_EX + f"  Avg Wind Speed: {avg_wind_speed} mph")
        type_out(Fore.LIGHTGREEN_EX + f"  Condition: {most_common_condition}")

    # Display temperature trend as an ASCII chart
    type_out(Fore.LIGHTGREEN_EX + "\nTemperature Trend (°F):")
    daily_averages = [round(sum(details["temps"]) / len(details["temps"]), 1) for details in forecast_by_day.values()]
    chart = ascii_bar_chart(daily_averages, label="Avg Temp")
    type_out(Fore.LIGHTGREEN_EX + chart + Style.RESET_ALL)

# Display options menu
def main_menu():
    """
    Display the main menu with Matrix-style theme.
    """
    type_out(Fore.LIGHTGREEN_EX + "\nPlease choose an option:")
    type_out(Fore.LIGHTGREEN_EX + "1. User current location")
    type_out(Fore.LIGHTGREEN_EX + "2. Select a city manually")
    type_out(Fore.LIGHTGREEN_EX + "3. View today's weather")
    type_out(Fore.LIGHTGREEN_EX + "4. View 5-day forecast")
    type_out(Fore.LIGHTGREEN_EX + "5. Fun weather fact")
    type_out(Fore.LIGHTGREEN_EX + "6. Exit")

# Main application loop
def main():
    global city
    city = None
    show_intro()  # Ensure the intro is displayed at the start
    type_out(Fore.LIGHTGREEN_EX + Back.BLACK + "Welcome to the Comprehensive Weather App!")
    while True:
        main_menu()
        choice = input(Fore.LIGHTGREEN_EX + "Your choice: " + Style.RESET_ALL)

        if choice == "1":
            option_one()
        elif choice == "2":
            option_two()
        elif choice == "3":
            display_ascii("3")
            if not city:
                type_out(Fore.RED + "Please select a city first.")
                continue
            weather_data = get_weather(city)
            if weather_data:
                display_weather(weather_data)
        elif choice == "4":
            if not city:
                type_out(Fore.RED + "Please select a city first.")
                continue
            forecast_data = requests.get(FORECAST_URL, params={"q": city, "appid": API_KEY, "units": "imperial"}).json()
            if "list" in forecast_data:
                display_forecast(forecast_data)
            else:
                type_out(Fore.RED + "Unable to fetch forecast data.")

        elif choice == "5":
            display_ascii("5")
            type_out(Fore.LIGHTGREEN_EX + weather_fun_fact())

        elif choice == "6":
            display_ascii("6")
            type_out(Fore.LIGHTGREEN_EX + "Goodbye! Stay safe!")
            break
        else:
            type_out(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
