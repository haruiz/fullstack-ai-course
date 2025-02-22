import requests
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from .env file
load_dotenv(find_dotenv())

def get_temperature(city_name):

    # Get the API key from the environment variables
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    # OpenWeatherMap API endpoint for current weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    # Send a GET request to the API
    response = requests.get(url)
    print(response.content)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the temperature from the JSON data
        temperature = data['main']['temp']
    
        # Return the temperature
        return temperature
    else:
        # Return an error message if something went wrong
        return f"Error: {response.status_code}, Unable to get data."

if __name__ == "__main__":
    city_name = "San Francisco"  # Change this to your desired location
    temperature = get_temperature(city_name)
    print(f"The current temperature in {city_name} is {temperature}°C.")
