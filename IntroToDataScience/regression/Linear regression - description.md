Decision tree regression - description
Steps:
1)Loaded raw dataset from https://data.tuik.gov.tr/Bulten/Index?p=House-Sales-Statistics-April-2023-49520&dil=2
2)Manually transformed(the file looked like a pdf before that), save to file "property_raw_table.csv"
3)Run preprocess_property_data.py
4)Run melt_data_and_plot.py
5)Run linear_regression.py
6)Run visualize_predictions.py
7)Obtain files:    
    - melted.csv // Data in format: Year, Month, Country, Sales
    - melted_predicted_2023.csv // Predictions data in format 2023, Month, Country, Sales
    - out.csv // merged state of the existing and predicted data to run visualization
    - out.png // Trend graph for property sales to foreigners in Turkiye in 2015-2023