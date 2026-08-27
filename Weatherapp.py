import requests
import os 
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")  # <-- Replace this with your actual API key
BASE_URL = "http://api.weatherapi.com/v1/current.json"

city = input("Enter the name of the city here: ")

params = {
    "key": API_KEY,
    "q": city,
    "aqi": "no"
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    temp = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    sentence=f"The temperature in {city} is {temp}°C and the weather is {condition}"
    command=f'''PowerShell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{sentence}');"'''
    os.system(command)
else:
    print(f"City not found or API error: {response.status_code}")
    
