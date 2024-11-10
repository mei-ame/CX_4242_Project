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
    airport_dict = {}
    for t in textlist:
        if float(t[-1]) != 0 and float(t[-2]) != 0:
            if t[1] == "N/A":
                airport_dict[t[0]] = {"Latitude": float(t[-2]),"Longitude": float(t[-1]), "Airport Name": t[3]}
            else:
                airport_dict[t[1]] = {"Latitude": float(t[-2]),"Longitude": float(t[-1]), "Airport Name": t[3]}
    # airport_dict = {t[1]: {"Latitude": float(t[-2]),"Longitude": float(t[-1]), "Airport Name": t[3]} for t in textlist}
    # print(sorted(airport_dict.keys()))
    # print([t for t in airport_dict.keys() if float(airport_dict[t]["Latitude"]) == 0 and float(airport_dict[t]["Longitude"]) == 0])
    if airport_code:
        return (airport_dict[airport_code]["Latitude"], airport_dict[airport_code]["Longitude"])
    else:
        return None
    
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