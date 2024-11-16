from serpapi import GoogleSearch

# Your SerpAPI API key
# API_KEY = "b637153e8613b18fc81533dfbf72045c9b43cbdd25323736bc3009ee6c38435a"
# API_KEY = "8e3b97559f70aeb1a2d6f78da4ca024bab7525e316361ac1c955016a16136cf7"
API_KEY = "a9deee9173656ca6302d2fed79e2b999494e4e0bcd7d177aad40ea88be63aa17"

# Function to search flights using inputs
def search_flights(departure_id, arrival_id, outbound_date, return_date, currency, max_price=None, min_time=None, max_time=None, departure_token=None):
    params = {
        "api_key": API_KEY,
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": currency,
    }

    # Add optional parameters if provided
    if max_price:
        params["price_max"] = max_price
    if min_time:
        params["min_time"] = min_time
    if max_time:
        params["max_time"] = max_time
    if departure_token:
        params["departure_token"] = departure_token

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Parse the best flights data
        if "best_flights" in results:
            flight_details = []
            for flight in results["best_flights"]:
                flight_info = {
                    "total_duration": flight.get("total_duration"),
                    "price": flight.get("price"),
                    "type": flight.get("type"),
                    "airline_logo": flight.get("airline_logo"),
                    "layovers": [
                        {
                            "name": layover["name"],
                            "duration": layover["duration"]
                        } for layover in flight.get("layovers", [])
                    ],
                    "flights": [
                        {
                            "departure_airport": flight_leg["departure_airport"]["name"],
                            "departure_time": flight_leg["departure_airport"]["time"],
                            "arrival_airport": flight_leg["arrival_airport"]["name"],
                            "arrival_time": flight_leg["arrival_airport"]["time"],
                            "airline": flight_leg["airline"],
                            "flight_number": flight_leg["flight_number"],
                            "duration": flight_leg["duration"],
                            "airplane": flight_leg["airplane"],
                            "travel_class": flight_leg.get("travel_class"),
                            "legroom": flight_leg.get("legroom"),
                        } for flight_leg in flight.get("flights", [])
                    ],
                    "departure_token": flight.get("departure_token")
                }
                flight_details.append(flight_info)
            return flight_details
        else:
            return "No flights found."
    except Exception as e:
        return str(e)