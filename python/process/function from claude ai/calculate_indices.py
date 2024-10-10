import pandas as pd
import numpy as np
from scipy.stats import norm

def calculate_spei(rainfall_data, evaporation_data, temperature_data):
    def thornthwaite_pet(temp_mean):
        I = np.sum((temp_mean / 5) ** 1.514)
        a = 6.75e-7 * I**3 - 7.71e-5 * I**2 + 1.792e-2 * I + 0.49239
        pet = 16 * ((10 * temp_mean / I) ** a)
        return pet

    stations = rainfall_data['station'].unique()
    all_spei_results = pd.DataFrame()

    for station in stations:
        station_rainfall = rainfall_data[rainfall_data['station'] == station]
        station_temperature = temperature_data[temperature_data['station'] == station]

        if station_rainfall.empty or station_temperature.empty:
            print(f"Warning: No data for station {station}")
            continue

        station_temperature['pet'] = station_temperature['monthly_average'].apply(thornthwaite_pet)
        combined_data = station_rainfall.merge(station_temperature[['datetime', 'pet']], on='datetime', how='inner')
        combined_data['w'] = combined_data['rainfall'] - combined_data['pet']

        mean_w = combined_data['w'].mean()
        std_w = combined_data['w'].std()
        combined_data['spei'] = (combined_data['w'] - mean_w) / std_w

        all_spei_results = pd.concat([all_spei_results, combined_data[['station', 'datetime', 'pet', 'w', 'spei']]], ignore_index=True)

    return all_spei_results

def calculate_spi(cleaned_rainfall_data):
    cleaned_rainfall_data['rainfall'] = cleaned_rainfall_data['rainfall'].replace(['T', '-'], np.nan).astype(float)

    mean_rainfall = cleaned_rainfall_data['rainfall'].mean()
    std_rainfall = cleaned_rainfall_data['rainfall'].std()

    def calculate_spi_value(rainfall, mean, std):
        if np.isnan(rainfall):
            return np.nan
        if std == 0:
            return np.nan
        else:
            return (rainfall - mean) / std

    cleaned_rainfall_data['spi'] = cleaned_rainfall_data['rainfall'].apply(calculate_spi_value, args=(mean_rainfall, std_rainfall))
    all_spi = cleaned_rainfall_data[['station', 'datetime', 'spi']].copy()

    return all_spi