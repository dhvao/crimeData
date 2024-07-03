import pandas as pd
import os

# Replace 'path/to/folder' with the actual path where your CSV files are located
data_path = '/Users/dhvao/Desktop/Dissertation/archive'
all_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]  # Get all CSV files

# Combine all data into a single DataFrame
all_data = pd.DataFrame()
for filename in all_files:
    file_path = os.path.join(data_path, filename)
    data_chunk = pd.read_csv(file_path)
    # Extract county name from the file name (adjust the parsing based on your file naming convention)
    county_name = filename.split('.')[0]  # Assuming the county name is before the first dot in the file name
    data_chunk['County'] = county_name
    all_data = pd.concat([all_data, data_chunk], ignore_index=True)

# Group data by 'County' and 'Crime type', count occurrences
county_crime_counts = all_data.groupby(['County', 'Crime type']).size().reset_index(name='Count')

# Sort by count in descending order within each county
county_crime_counts.sort_values(by=['County', 'Count'], ascending=[True, False], inplace=True)

# Save the result to a CSV file with absolute path
save_path = '/Users/dhvao/Desktop/Dissertation/'
county_crime_counts.to_csv(os.path.join(save_path, 'county_crime_counts.csv'), index=False)
print(f"County crime counts table saved as '{os.path.join(save_path, 'county_crime_counts.csv')}'")
