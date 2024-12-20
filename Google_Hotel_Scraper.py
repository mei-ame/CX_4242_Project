from serpapi import GoogleSearch

# Your SerpAPI API key
API_KEY = "0833d129d4d470155409dd49357d8fdaeccc304f1c64027d7d8cd83aa92f94de"

# Function to search hotels using inputs
def search_hotels(location, check_in_date, check_out_date, currency="USD", max_price=None, min_price=None, min_rating=None, amenities=None):
    params = {
        "api_key": API_KEY,
        "engine": "google_hotels",
        "q": location,  # Location or query for the hotel search
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "currency": currency,
        "sort_by": 3 if max_price else None  # Sort by lowest price if max_price is set
    }

    # Add optional parameters if provided
    if max_price:
        params["max_price"] = max_price  # Updated according to SerpApi documentation
    if min_price:
        params["min_price"] = min_price  # New parameter for lower bound of price range
    if min_rating:
        params["rating"] = min_rating  # Updated to match the correct parameter for minimum rating (options: 7, 8, 9)
    if amenities:
        params["amenities"] = ','.join(map(str, amenities))  # Format amenities as a comma-separated string

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        # Parse the hotel results data
        if "properties" in results:
            hotel_details = []
            for hotel in results["properties"]:
                hotel_info = {
                    "name": hotel.get("name"),
                    "price_per_night": hotel.get("rate_per_night", {}).get("lowest"),
                    "total_price": hotel.get("total_rate", {}).get("lowest"),
                    "rating": hotel.get("overall_rating"),
                    "latitude": hotel.get("gps_coordinates", {}).get("latitude"),  # Extract latitude
                    "longitude": hotel.get("gps_coordinates", {}).get("longitude"),  # Extract longitude
                    "amenities": hotel.get("amenities", []),
                    "thumbnail": hotel.get("images", [{}])[0].get("thumbnail") if hotel.get("images") else None
                }
                hotel_details.append(hotel_info)
            return hotel_details
        else:
            return "No hotels found."
    except Exception as e:
        return f"Error: {e}"
