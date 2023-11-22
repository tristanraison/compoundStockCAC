# Import necessary libraries
import yfinance as yf
import os
import pandas as pd
import matplotlib.pyplot as plt

# Import custom function from another file
from data_getter import get_nearest_value

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the data file
data_file_path = os.path.join(
    script_dir, 'data_cac_gtr', 'CAC 40 Gross Total Return - Données Historiques.csv')

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(data_file_path, thousands='.', decimal=',')

# Convert the "Date" column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Convert numeric columns to numeric format (commented out)
numeric_columns = ['Dernier', 'Ouv.', 'Plus Haut', 'Plus Bas']
# df[numeric_columns] = df[numeric_columns].apply(lambda x: pd.to_numeric(
#     x.str.replace(',', '').str.replace('.', ''), errors='coerce'))

# Remove specified columns (case-sensitive)
columns_to_remove = ['Ouv.', 'Plus Haut', 'Plus Bas']
df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])

# Example usage of get_nearest_value function
first_investment_date = '01/01/2000'
investment_period = 23
reduction_factor = -.0
monthlyInvestedInEstate = 2150
monthlyInvestedCapital = monthlyInvestedInEstate * (1+reduction_factor)


# Calculate start and end dates based on the investment period
start_date = pd.to_datetime(first_investment_date, format='%d/%m/%Y')
end_date = start_date + pd.DateOffset(months=investment_period*12)

# Generate a date schedule for the investment period
date_schedule = pd.date_range(
    start=start_date, end=end_date, freq='MS').strftime('%d/%m/%Y')

# Use the custom function to get the nearest value in the DataFrame
nearest_value = get_nearest_value(df, first_investment_date)

# Get the "Dernier" value for each date in the schedule
result_list = []
prev_value = None

# Initialize variables for compounded capital calculation
compounded_capital = 0
invested_capital = 0
compounded_capital_list = []


for date in date_schedule:
    nearest_value = get_nearest_value(df, date)

    # Calculate yield for each year (skip for the first entry)
    # Calculate yield for each year (skip for the first entry)
    if prev_value is not None:
        yield_value = nearest_value / prev_value
    else:
        yield_value = 1

    prev_value = nearest_value

    # Update compounded capital for the next iteration
    compounded_capital = (compounded_capital +
                          monthlyInvestedCapital) * yield_value

    invested_capital += monthlyInvestedCapital

    # Append the result to the list
    compounded_capital_list.append(
        {'Date': date, 'Invested Capital': invested_capital, 'Compounded Capital': compounded_capital, "Month yeild": yield_value-1})

# Display the compounded capital list
print("\nCompounded Capital List:")
for result in compounded_capital_list:
    print(result)


# Convert the result list to a DataFrame
result_df = pd.DataFrame(compounded_capital_list)


# Plotting the chart
plt.figure(figsize=(10, 6))
plt.plot(result_df['Date'], result_df['Compounded Capital'],
         label='Compounded Capital')
plt.plot(result_df['Date'], result_df['Invested Capital'],
         label='Invested Capital')
plt.title('Compounded Capital and Invested Capital Over Time')
plt.xlabel('Date')
plt.ylabel('Capital')
plt.legend()
plt.show()
