import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Read the CSV files
df = pd.read_csv("melted.csv")

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Extract year and month from 'Date' column
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Filter data for 2023
df_2023 = df[df['Year'] == 2023]

# Create a new DataFrame to store the predicted values
df_predictions = pd.DataFrame(columns=['Country', 'Year', 'Month', 'Sales'])

# Train the regression model for each country
countries = df['Country'].unique()

for country in countries:
    # Filter data for the current country
    df_country = df[df['Country'] == country]
    
    # Train the regression model
    X_train = df_country[['Year', 'Month']].values
    y_train = df_country['Sales'].values.reshape(-1, 1)
    regression = LinearRegression()
    regression.fit(X_train, y_train)
    
    # Predict 2023 values for each month
    X_2023 = np.array([[2023, month] for month in range(1, 13)])
    y_2023_pred = regression.predict(X_2023)
    
    # Create a DataFrame for the predictions
    df_country_pred = pd.DataFrame({
        'Country': country,
        'Year': 2023,
        'Month': range(1, 13),
        'Sales': y_2023_pred.flatten()
    })
    
    # Append the country's predictions to the main predictions DataFrame
    df_predictions = pd.concat([df_predictions, df_country_pred], ignore_index=True)

# Print the predictions for 2023
df_predictions.to_csv("melted_predicted_2023.csv")
