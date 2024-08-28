import pandas as pd

# Load the dataset
data = pd.read_csv('property_raw_table.csv')

# Split column titles and keep only the first part, capitalized
data.columns = data.columns.str.split(' ').str[0].str.capitalize()

# Extract the part before the hyphen "-" in the "Country" column
data['Country'] = data['Country'].str.split('-').str[0]

# Preprocess the data - Remove spaces from all columns
data = data.replace(' ', '', regex=True)

# Extract the data for the year 2023
data_2023 = data[data['Year'] == 2023].copy()
# Remove the data for the year 2023
data = data[data['Year'] != 2023].copy()

# Save the modified data to a new CSV file
data.to_csv('data_without_2023.csv', index=False)

# Save the 2023 data to a new CSV file
data_2023.to_csv('actual_data_January_April_2023.csv', index=False)
