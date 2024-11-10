import math
import requests
from haversine import haversine, Unit

# Function to get latitude and longitude from airport code
# def get_airport_location(airport_code):
#     # Using Nominatim API from OpenStreetMap for simplicity
#     url = f"https://nominatim.openstreetmap.org/search?q={airport_code}&format=json&limit=1"
#     response = requests.get(url)
#     data = response.json()
    
#     if data:
#         lat = float(data[0]["lat"])
#         lon = float(data[0]["lon"])
#         return (lat, lon)
#     else:
#         return None

def get_airport_location(airport_code):
    with open("GlobalAirportDatabase.txt", "r") as infile: 
        text = infile.readlines()
        textlist = [line.strip().split(":") for line in text]

        # for row in textlist[1::2]:
        #     racer_dict[row[0]] = row[1]
    airport_dict = {t[1]: {"Latitude": float(t[-2]),"Longitude": float(t[-1]), "Airport Name": t[3]} for t in textlist}
    return (airport_dict[airport_code]["Latitude"], airport_dict[airport_code]["Longitude"])
    
    # json.dump(racer_dict, open('abbrevs.json', 'w'))

# Function to calculate distance between airport and hotel location
def calculate_distance(airport_code, hotel_lat, hotel_lon):
    airport_location = get_airport_location(airport_code)
    
    if not airport_location:
        raise ValueError("Invalid airport code or location not found.")
    
    airport_lat, airport_lon = airport_location
    hotel_location = (hotel_lat, hotel_lon)
    
    # Calculate distance in kilometers
    distance_km = haversine((airport_lat, airport_lon), hotel_location, unit=Unit.MILES)
    return distance_km

print(calculate_distance("HOU", -8.808104, 115.22827729999999))