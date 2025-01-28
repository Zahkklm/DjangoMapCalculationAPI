import pandas as pd
from geopy.geocoders import OpenCage
import time

# Replace with your OpenCage API key
api_key = '6971f7b651ba45049b778d1bc54ce5c7'
geolocator = OpenCage(api_key)

# Read the CSV file
fuel_prices = pd.read_csv('fuel_prices.csv')

# Function to geocode an address
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None

# Create new columns for latitude and longitude
fuel_prices['Latitude'] = None
fuel_prices['Longitude'] = None

# Geocode each address and update the DataFrame
for index, row in fuel_prices.iterrows():
    address = f"{row['Address']}, {row['City']}, {row['State']}"
    lat, lng = geocode_address(address)

    fuel_prices.at[index, 'Latitude'] = lat
    fuel_prices.at[index, 'Longitude'] = lng
    time.sleep(1)  # To avoid hitting the API rate limit

# Write the updated DataFrame to a new CSV file
fuel_prices.to_csv('fuel_prices_with_lat_lng.csv', index=False)