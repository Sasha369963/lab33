import pandas as pd
from urllib import request
from os import listdir, makedirs, walk, path
from shutil import rmtree
from datetime import datetime
from re import search

def clean_and_prepare_folder(folder_path):
    """Clean the folder if not empty and prepare it for new data."""
    if path.exists(folder_path):
        if listdir(folder_path):
            rmtree(folder_path)
        makedirs(folder_path, exist_ok=True)
    else:
        makedirs(folder_path, exist_ok=True)

def download_weather_data(region_id):
    """Download weather data for a specific region ID."""
    url = f'https://example.com/weather/data?regionID={region_id}&yearStart=1980&yearEnd=2024&type=Summary'

    try:
        data = request.urlopen(url).read().decode('utf-8')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        with open(f'data/weather_region_{region_id}_{timestamp}.csv', 'w') as file:
            file.write(data)

    except Exception as e:
        print(f"Error downloading data for region ID {region_id}: {e}")

def process_csv_to_dataframe(file_path, norm_region_id):
    """Process a CSV file and return a cleaned DataFrame."""
    columns = ['Year', 'Month', 'Temperature', 'Rainfall', 'Humidity', 'WindSpeed', 'Region', 'Unused']
    df = pd.read_csv(file_path, header=1, names=columns)
    
    # Clean and process data
    df = df[df['Temperature'] != -1]  # Remove invalid temperature rows
    df['Region'] = norm_region_id
    df = df.drop(columns=['Unused'])  # Drop unnecessary columns
    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].astype(int)

    return df

def collect_file_paths(directory):
    """Collect all file paths from a given directory."""
    paths = []
    for root, dirs, files in walk(directory):
        for file in files:
            paths.append(path.join(root, file))
    return paths

def extract_region_id(file_path):
    """Extract region ID from the content of a file."""
    with open(file_path, 'r') as file:
        match = search(r'Region\s*=\s*(\d+)', file.readline())
        if match:
            return int(match.group(1))
        else:
            raise ValueError("Region ID not found in file")

# Mapping of old region IDs to normalized IDs
region_id_mapping = {
    1: 101, 2: 102, 3: 103, 4: 104, 5: 105,
    6: 106, 7: 107, 8: 108, 9: 109, 10: 110,
    11: 111, 12: 112, 13: 113, 14: 114, 15: 115,
    16: 116, 17: 117, 18: 118, 19: 119, 20: 120
}

# Example usage
if __name__ == "__main__":
    data_folder = "data"
    clean_and_prepare_folder(data_folder)

    # Download and process data for each region
    for old_id, new_id in region_id_mapping.items():
        download_weather_data(old_id)

    # Process files into DataFrames
    all_paths = collect_file_paths(data_folder)
    for file_path in all_paths:
        region_id = extract_region_id(file_path)
        normalized_id = region_id_mapping.get(region_id, region_id)
        df = process_csv_to_dataframe(file_path, normalized_id)
        print(df.head())
