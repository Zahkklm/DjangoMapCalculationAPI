import pandas as pd

def deduplicate_truckstops(input_file, output_file):
    """
    Remove duplicate entries from truckstop data based on OPIS Truckstop ID.
    Keeps the first occurrence of each ID.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Remove duplicates based on 'OPIS Truckstop ID', keeping first occurrence
    df_deduplicated = df.drop_duplicates(subset=['OPIS Truckstop ID'], keep='first')
    
    # Save the deduplicated data to a new CSV file
    df_deduplicated.to_csv(output_file, index=False)
    
    # Print statistics
    total_rows = len(df)
    unique_rows = len(df_deduplicated)
    duplicates_removed = total_rows - unique_rows
    
    print(f"Original rows: {total_rows}")
    print(f"Rows after deduplication: {unique_rows}")
    print(f"Duplicates removed: {duplicates_removed}")

if __name__ == "__main__":
    input_file = "fuel_prices.csv"  
    output_file = "fuel_prices_deduplicated.csv"  
    
    deduplicate_truckstops(input_file, output_file)