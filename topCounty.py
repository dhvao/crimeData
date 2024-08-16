import os
import pandas as pd

# Define the path to the folder containing the CSV files
data_path = '/Users/dhvao/Desktop/Dissertation/archive'

# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]

# Initialize an empty DataFrame to hold all data
all_data = pd.DataFrame()

# Process each CSV file
for file_name in csv_files:
    file_path = os.path.join(data_path, file_name)
    # Read the CSV file into a DataFrame
    data_chunk = pd.read_csv(file_path)
    # Extract the county name from the file name (assuming the county name is the file name without extension)
    county_name = os.path.splitext(file_name)[0]
    # Add the county name as a new column in the DataFrame
    data_chunk['County'] = county_name
    # Append the data to the main DataFrame
    all_data = pd.concat([all_data, data_chunk], ignore_index=True)

# Group the data by 'County' and 'Crime type' and count occurrences
county_crime_counts = all_data.groupby(['County', 'Crime type']).size().reset_index(name='Count')

# Identify the county with the highest count for each crime type
top_county_for_crime = county_crime_counts.loc[county_crime_counts.groupby('Crime type')['Count'].idxmax()]

# Define the output file path
output_csv_path = '/Users/dhvao/Desktop/Dissertation/top_county_for_each_crime.csv'

# Save the result to a CSV file
top_county_for_crime.to_csv(output_csv_path, index=False)

# Print a confirmation message
print(f"Top county for each crime type saved as '{output_csv_path}'")
