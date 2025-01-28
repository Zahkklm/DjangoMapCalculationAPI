import pandas as pd
import requests
import time
from urllib.parse import quote

def geocode_address_photon(address, city, state):
    """
    Geocode an address using Photon
    """
    # Combine address components
    full_address = f"{address}, {city}, {state}, USA"
    
    # URL encode the address
    encoded_address = quote(full_address)
    
    # Create the URL (Photon's endpoint)
    url = f"http://photon.komoot.io/api/?q={encoded_address}&limit=1"
    
    try:
        # Add a small delay to be nice to the API
        time.sleep(0.5)
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('features') and len(data['features']) > 0:
            # Get coordinates from the first result
            coordinates = data['features'][0]['geometry']['coordinates']
            # Photon returns [lon, lat], but we want [lat, lon]
            return (coordinates[1], coordinates[0])
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
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Add new columns for coordinates
    df['Latitude'] = None
    df['Longitude'] = None
    
    # Process each row
    for index, row in df.iterrows():
        print(f"Processing: {row['Truckstop Name']}")
        
        result = geocode_address_photon(row['Address'], row['City'], row['State'])
        
        if result:
            df.at[index, 'Latitude'] = result[0]
            df.at[index, 'Longitude'] = result[1]
    
    # Save results to new CSV
    df.to_csv(output_file, index=False)
    
    # Print summary
    total_rows = len(df)
    geocoded_rows = df['Latitude'].notna().sum()
    print(f"\nGeocoding Summary:")
    print(f"Total rows processed: {total_rows}")
    print(f"Successfully geocoded: {geocoded_rows}")
    print(f"Failed to geocode: {total_rows - geocoded_rows}")

if __name__ == "__main__":
    input_file = "fuel_prices.csv"  
    output_file = "fuel_prices_geocoded.csv" 
    
    process_csv(input_file, output_file)