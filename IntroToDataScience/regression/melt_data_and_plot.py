import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV files
df_actual = pd.read_csv("data_without_2023.csv")


# Merge df1 and df2
merged_df = df_actual
# Melt the dataframe to convert columns into a time series format
melted_df = pd.melt(merged_df, id_vars=['Country', 'Year'], var_name='Month', value_name='Sales')
melted_df.to_csv("melted.csv")
# Combine the 'Month' and 'Year' columns into a single column
melted_df['Date'] = pd.to_datetime(melted_df['Year'].astype(str) + '-' + melted_df['Month'], format='%Y-%B')
melted_df = melted_df.drop(['Year', 'Month'], axis=1)

# Sort the dataframe by country and date
melted_df = melted_df.sort_values(['Country', 'Date']).reset_index(drop=True)

# Calculate the ranking for each country
ranking_df = melted_df.groupby('Country')['Sales'].sum().sort_values(ascending=False).reset_index()
ranking_df['Rank'] = ranking_df.index + 1
ranking_dict = ranking_df.set_index('Country')['Rank'].to_dict()


# Get the top 12 countries
top_countries = ranking_df.head(12)['Country'].tolist()

# Filter the melted_df to keep only the top 12 countries
melted_df_top = melted_df[melted_df['Country'].isin(top_countries)]

# Plot a line for each country with ranking on the legend
plt.figure(figsize=(12, 8))

for country, group in melted_df_top.groupby('Country'):
    plt.plot(group['Date'], group['Sales'], label=f"{country} (Rank {ranking_dict[country]})")

plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Property sales to foreigners in Tukiye 2015-2023')
plt.legend()
plt.axvline(pd.to_datetime('2023'), color='r', linestyle='--', label='2023')
plt.xticks(rotation=45)
plt.show()