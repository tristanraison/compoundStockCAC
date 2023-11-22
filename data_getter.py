import yfinance as yf
import os
import pandas as pd


def get_nearest_value(df, target_date):
    # Convert target_date to datetime
    target_date = pd.to_datetime(target_date, format='%d/%m/%Y')

    # Find the index of the nearest date in the DataFrame
    nearest_index = (df['Date'] - target_date).abs().idxmin()

    # Get the value in the "Dernier" column at the nearest index
    nearest_value = df.loc[nearest_index, 'Dernier']

    return nearest_value
