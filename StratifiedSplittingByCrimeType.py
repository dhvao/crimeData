import pandas as pd
import os

# Set paths for data and save location
data_path = '/Users/dhvao/Desktop/Dissertation/archive'
save_path = '/Users/dhvao/Desktop/Dissertation/'

# Get list of CSV files in the specified directory
csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]

# Print the list of CSV files
print("List of CSV files found:")
for file in csv_files:
    print(file)

# Combine all data from CSV files into a single DataFrame
all_data = pd.concat(
    (pd.read_csv(os.path.join(data_path, f)) for f in csv_files), 
    ignore_index=True
)

# Print summary of loaded data
print("\nAll CSV files have been loaded.")
print(f"Total rows in combined data: {len(all_data)}")
print(f"Column names: {list(all_data.columns)}")

# Sort data by 'Crime type'
stratified_data = all_data.sort_values(by='Crime type')
print("\nData has been sorted by 'Crime type'.")

# Function to split data by 'Crime type'
def split_by_crime_type(data, train_ratio=0.7):
    training_data = pd.DataFrame()
    testing_data = pd.DataFrame()

    # Group data by 'Crime type' and split into training and testing datasets
    grouped = data.groupby('Crime type')
    
    for crime_type, group in grouped:
        crime_training_size = int(train_ratio * len(group))
        crime_training_data = group.sample(crime_training_size, random_state=42)
        crime_testing_data = group.drop(crime_training_data.index)

        training_data = pd.concat([training_data, crime_training_data], ignore_index=True)
        testing_data = pd.concat([testing_data, crime_testing_data], ignore_index=True)

        print(f"Processed Crime Type: '{crime_type}'")
        print(f"Training set size for '{crime_type}': {len(crime_training_data)}")
        print(f"Testing set size for '{crime_type}': {len(crime_testing_data)}\n")

    return training_data, testing_data

# Split data and print details
training_data, testing_data = split_by_crime_type(stratified_data)

print(f"\nTotal data points: {len(stratified_data)}")
print(f"Training data points: {len(training_data)}")
print(f"Testing data points: {len(testing_data)}")

# Save the split datasets to CSV files
training_file_path = os.path.join(save_path, 'training_data.csv')
testing_file_path = os.path.join(save_path, 'testing_data.csv')

training_data.to_csv(training_file_path, index=False)
testing_data.to_csv(testing_file_path, index=False)

print(f"\nTraining data saved to: {training_file_path}")
print(f"Testing data saved to: {testing_file_path}")
