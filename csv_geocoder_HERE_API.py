import pandas as pd
import requests
import time
from urllib.parse import quote
import os
from datetime import datetime

# HERE API Configuration
API_KEY = "_HJVITExiRDmHnpP9t8G2Ic88P-qA2YH5aV6qb8J1d8" 

def geocode_address_here(address, city, state):
    """
    Geocode an address using HERE Geocoding API
    """
    # Combine address components
    full_address = f"{address}, {city}, {state}, USA"
    
    # Create the URL
    base_url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {
        'q': full_address,
        'apiKey': API_KEY,
        'limit': 1
    }
    
    try:
        # Add a small delay between requests
        time.sleep(0.2)
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('items') and len(data['items']) > 0:
            # Get coordinates from the first result
            position = data['items'][0]['position']
            return (position['lat'], position['lng'])
        else:
            print(f"No results found for address: {full_address}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error geocoding address: {full_address}")
        print(f"Error details: {e}")
        return None

def process_csv(input_file, output_file):
    """
    Process CSV file and add geocoding results
    """
    # Verify API key is set
    if API_KEY == "YOUR_API_KEY_HERE":
        raise ValueError("Please set your HERE API key in the script")
    
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Add new columns for coordinates
    df['Latitude'] = None
    df['Longitude'] = None
    
    # Add columns for geocoding metadata
    df['Geocoding_Timestamp'] = None
    df['Geocoding_Status'] = None
    
    # Process each row
    total_rows = len(df)
    for index, row in df.iterrows():
        print(f"Processing {index + 1}/{total_rows}: {row['Truckstop Name']}")
        
        result = geocode_address_here(row['Address'], row['City'], row['State'])
        
        if result:
            df.at[index, 'Latitude'] = result[0]
            df.at[index, 'Longitude'] = result[1]
            df.at[index, 'Geocoding_Status'] = 'SUCCESS'
        else:
            df.at[index, 'Geocoding_Status'] = 'FAILED'
            
        df.at[index, 'Geocoding_Timestamp'] = datetime.now().isoformat()
    
    # Save results to new CSV
    df.to_csv(output_file, index=False)
    
    # Print summary
    total_rows = len(df)
    geocoded_rows = df['Latitude'].notna().sum()
    print(f"\nGeocoding Summary:")
    print(f"Total rows processed: {total_rows}")
    print(f"Successfully geocoded: {geocoded_rows}")
    print(f"Failed to geocode: {total_rows - geocoded_rows}")
    
    # Save failed geocoding attempts to separate file for review
    failed_rows = df[df['Geocoding_Status'] == 'FAILED']
    if len(failed_rows) > 0:
        failed_file = f"failed_geocoding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        failed_rows.to_csv(failed_file, index=False)
        print(f"Failed geocoding attempts saved to: {failed_file}")

def validate_api_key():
    """
    Test the API key with a simple request
    """
    test_address = "350 5th Ave, New York, NY, USA"
    base_url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {
        'q': test_address,
        'apiKey': API_KEY,
        'limit': 1
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        print("API key validation successful!")
        return True
    except requests.exceptions.RequestException as e:
        print("API key validation failed!")
        print(f"Error details: {e}")
        return False

if __name__ == "__main__":
    input_file = "fuel_prices - Copy (3).csv"  
    output_file = "fuelprices_HERE_geocoded.csv"  
    
    # Validate API key before processing
    if validate_api_key():
        process_csv(input_file, output_file)
    else:
        print("Please check your HERE API key and try again.")