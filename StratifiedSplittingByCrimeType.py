import pandas as pd
import random
import os

# Replace 'path/to/folder' with the actual path where your CSV files are located
data_path = '/Users/dhvao/Desktop/Dissertation/archive'
all_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]  # Get all CSV files

# Print the list of CSV files
print("List of CSV files:")
print(all_files)

# Combine all data into a single DataFrame
all_data = pd.DataFrame()
for filename in all_files:
    file_path = os.path.join(data_path, filename)
    data_chunk = pd.read_csv(file_path)
    all_data = pd.concat([all_data, data_chunk], ignore_index=True)

# Print loaded CSV files information
print("Loaded all CSV files")
print("Number of rows in all_data:", len(all_data))
print("Column names:", all_data.columns)

# Sort data by Crime Type
stratified_data = all_data.sort_values(by='Crime type')
print("Data sorted by Crime type")
total_data_points = len(stratified_data)
training_size = int(0.7 * total_data_points)  # 70% for training
testing_size = total_data_points - training_size  # 30% for testing

def split_by_crime_type(data, training_size, testing_size):
    training_data = pd.DataFrame()
    testing_data = pd.DataFrame()
    current_crime_type = None
    current_crime_data = pd.DataFrame()

    for index, row in data.iterrows():
        crime_type = row['Crime type']

        # If it's a new crime type, initialize variables
        if crime_type != current_crime_type:
            current_crime_type = crime_type
            current_crime_data = data[data['Crime type'] == crime_type]

            # Split data for the current crime type
            crime_training_size = int(0.7 * len(current_crime_data))
            crime_testing_size = len(current_crime_data) - crime_training_size
            crime_training_data = current_crime_data.sample(crime_training_size, random_state=42)  # Ensure reproducibility
            crime_testing_data = current_crime_data.drop(crime_training_data.index)

            # Update training and testing DataFrames
            training_data = pd.concat([training_data, crime_training_data], ignore_index=True)
            testing_data = pd.concat([testing_data, crime_testing_data], ignore_index=True)

            # Additional print statements for debugging
            print(f"Processing Crime Type: {crime_type}")
            print(f"Training size for {crime_type}: {len(crime_training_data)}")
            print(f"Testing size for {crime_type}: {len(crime_testing_data)}")

    return training_data, testing_data


# Print information about the split
print("Total data points:", total_data_points)
print("Training size:", training_size)
print("Testing size:", testing_size)

training_data, testing_data = split_by_crime_type(stratified_data.copy(), training_size, testing_size)

# Print information about the generated datasets
print("Number of rows in training_data:", len(training_data))
print("Number of rows in testing_data:", len(testing_data))

# Save datasets to CSV files with absolute paths
save_path = '/Users/dhvao/Desktop/Dissertation/'
training_data.to_csv(os.path.join(save_path, 'training_data.csv'), index=False)
testing_data.to_csv(os.path.join(save_path, 'testing_data.csv'), index=False)
print(f"Training and testing datasets saved as '{os.path.join(save_path, 'training_data.csv')}' and '{os.path.join(save_path, 'testing_data.csv')}'")
