import pandas as pd
import os
import matplotlib.pyplot as plt

# Replace 'path/to/folder' with the actual path where your CSV files are located
data_path = '/Users/dhvao/Desktop/Dissertation/archive'
output_path = '/Users/dhvao/Desktop/Dissertation/pie_charts'

# Create the output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

streets = [
    'cleveland', 'west-yorkshire', 'wiltshire', 'norfolk', 'north-wales',
    'north-yorkshire', 'northamptonshire', 'northern-ireland', 'northumbria',
    'nottinghamshire', 'south-wales', 'south-yorkshire', 'staffordshire',
    'suffolk', 'surrey', 'sussex', 'thames-valley', 'warwickshire',
    'west-mercia', 'west-midlands', 'bedfordshire', 'btp', 'cambridgeshire',
    'cheshire', 'city-of-london', 'cumbria', 'derbyshire', 'dorset', 'durham',
    'dyfed-powys', 'essex', 'gloucestershire', 'gwent', 'hampshire',
    'hertfordshire', 'humberside', 'kent', 'lancashire', 'leicestershire',
    'lincolnshire', 'merseyside', 'metropolitan', 'avon-and-somerset'
]

for street in streets:
    file_name = f'2023-01-{street}-street.csv'
    file_path = os.path.join(data_path, file_name)

    if os.path.exists(file_path):
        # Read the CSV file
        data = pd.read_csv(file_path)

        # Group data by 'Crime type' and calculate the percentage distribution
        crime_distribution = data['Crime type'].value_counts(normalize=True) * 100

        # Create a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(crime_distribution, labels=crime_distribution.index, autopct='%1.1f%%', startangle=140)
        plt.title(f'Crime Distribution in {street.capitalize()} Street')

        # Save the pie chart
        output_file_path = os.path.join(output_path, f'{street}_pie_chart.png')
        plt.savefig(output_file_path)
        plt.close()
        print(f"Pie chart for {street.capitalize()} Street saved in '{output_file_path}'")
    else:
        print(f"File not found: {file_path}")

print("Pie charts generated for all streets.")
