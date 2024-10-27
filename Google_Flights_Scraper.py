# Your SerpAPI API key
API_KEY = "b637153e8613b18fc81533dfbf72045c9b43cbdd25323736bc3009ee6c38435a"

# Function to search flights using inputs
def search_flights(departure_id, arrival_id, outbound_date, return_date, currency, max_price=None, min_time=None, max_time=None):
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