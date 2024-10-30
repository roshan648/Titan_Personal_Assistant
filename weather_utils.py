# weather_utils.py

import requests
from urllib.parse import quote
from speech_utils import speak  # Ensure this import is correct

def get_location():
    ip_info_url = "https://ipinfo.io/json"
    try:
        response = requests.get(ip_info_url)
        response.raise_for_status()
        data = response.json()
        city = data.get('city', 'Unknown')
        return city
    except requests.RequestException as e:
        print(f"Error fetching location: {e}")
        return 'Unknown'

def get_weather(city):
    api_key = '23396aeb8098b60c343f93b12ca2a694'  # Replace with your valid API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()

        if data.get('cod') == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            speak(f"The current weather in {city} is {description} with a temperature of {temp} degrees Celsius.")
        else:
            speak(f"Failed to retrieve weather information. Error code: {data.get('cod')}.")
    except requests.RequestException as e:
        speak("An error occurred while fetching the weather information.")
        print(f"Error: {e}")  # Print the error for debugging
