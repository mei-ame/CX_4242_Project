import math
import requests
from haversine import haversine, Unit

# Function to get latitude and longitude from airport code
def get_airport_location(airport_code):
    # Using Nominatim API from OpenStreetMap for simplicity
    url = f"https://nominatim.openstreetmap.org/search?q={airport_code}&format=json&limit=1"
    response = requests.get(url)
    data = response.json()
    
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return (lat, lon)
    else:
        return None

# Function to calculate distance between airport and hotel location
def calculate_distance(airport_code, hotel_lat, hotel_lon):
    airport_location = get_airport_location(airport_code)
    
    if not airport_location:
        raise ValueError("Invalid airport code or location not found.")
    
    airport_lat, airport_lon = airport_location
    hotel_location = (hotel_lat, hotel_lon)
    
    # Calculate distance in kilometers
    distance_km = haversine((airport_lat, airport_lon), hotel_location, unit=Unit.KILOMETERS)
    return distance_km