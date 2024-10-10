import pandas as pd
import numpy as np

def load_humidity_data(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    humidity_data = pd.concat(dataframes, ignore_index=True)
    humidity_cleaned = humidity_data.copy()
    humidity_cleaned = humidity_cleaned.dropna()
    humidity = humidity_cleaned.drop('ความชื้นสัมพัทธ์(เปอร์เซ็นต์)', axis=1)
    
    humidity.rename(
        columns={**{
            f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
        },
        "Unnamed: 1": "station",
        "Unnamed: 2": "datetime",
        "Unnamed: 34": "humidity"},
        inplace=True
    )
    
    humidity['datetime'] = pd.to_datetime(humidity['datetime'], format='%b-%y')
    humidity['datetime'] = pd.to_datetime(humidity['datetime'], format='%d-%m-%Y')
    humidity['year'] = humidity['datetime'].dt.year
    humidity['month'] = humidity['datetime'].dt.month
    
    new_column_order = ['station', 'datetime', 'year', 'month'] + \
                       [f'day{i}' for i in range(1, 32)] + ['humidity']
    humidity = humidity[new_column_order]
    
    return humidity

def load_rainfall_data(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    rainfall_data = pd.concat(dataframes, ignore_index=True)
    rainfall_cleaned = rainfall_data.copy()
    rainfall_cleaned = rainfall_cleaned.dropna()
    rainfall = rainfall_cleaned.drop('ปริมาณฝน(มิลลิเมตร)', axis=1)
    
    rainfall.rename(
        columns={**{
            f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
        },
        "Unnamed: 1": "station",
        "Unnamed: 2": "datetime",
        "Unnamed: 34": "rainfall"},
        inplace=True
    )
    
    rainfall['datetime'] = pd.to_datetime(rainfall['datetime'], format='%b-%y')
    rainfall['datetime'] = pd.to_datetime(rainfall['datetime'], format='%d-%m-%Y')
    rainfall['year'] = rainfall['datetime'].dt.year
    rainfall['month'] = rainfall['datetime'].dt.month
    
    new_column_order = ['station', 'datetime', 'year', 'month'] + \
                       [f'day{i}' for i in range(1, 32)] + ['rainfall']
    rainfall = rainfall[new_column_order]
    
    return rainfall

def load_temperature_max_data(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    temperature_max_data = pd.concat(dataframes, ignore_index=True)
    temperature_max_cleaned = temperature_max_data.copy()
    temperature_max_cleaned = temperature_max_cleaned.dropna()
    temperature_max = temperature_max_cleaned.drop('อุณหภูมิสูงสุด(เซลเซียส)', axis=1)
    
    temperature_max.rename(
        columns={**{
            f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
        },
        "Unnamed: 1": "station",
        "Unnamed: 2": "datetime",
        "Unnamed: 34": "temperature_max"},
        inplace=True
    )
    
    temperature_max['datetime'] = pd.to_datetime(temperature_max['datetime'], format='%b-%y')
    temperature_max['datetime'] = pd.to_datetime(temperature_max['datetime'], format='%d-%m-%Y')
    temperature_max['year'] = temperature_max['datetime'].dt.year
    temperature_max['month'] = temperature_max['datetime'].dt.month
    
    new_column_order = ['station', 'datetime', 'year', 'month'] + \
                       [f'day{i}' for i in range(1, 32)] + ['temperature_max']
    temperature_max = temperature_max[new_column_order]
    
    return temperature_max

def load_temperature_min_data(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    temperature_min_data = pd.concat(dataframes, ignore_index=True)
    temperature_min_cleaned = temperature_min_data.copy()
    temperature_min_cleaned = temperature_min_cleaned.dropna()
    temperature_min = temperature_min_cleaned.drop('อุณหภูมิต่ำสุด(เซลเซียส)', axis=1)
    
    temperature_min.rename(
        columns={**{
            f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
        },
        "Unnamed: 1": "station",
        "Unnamed: 2": "datetime",
        "Unnamed: 34": "temperature_min"},
        inplace=True
    )
    
    temperature_min['datetime'] = pd.to_datetime(temperature_min['datetime'], format='%b-%y')
    temperature_min['datetime'] = pd.to_datetime(temperature_min['datetime'], format='%d-%m-%Y')
    temperature_min['year'] = temperature_min['datetime'].dt.year
    temperature_min['month'] = temperature_min['datetime'].dt.month
    
    new_column_order = ['station', 'datetime', 'year', 'month'] + \
                       [f'day{i}' for i in range(1, 32)] + ['temperature_min']
    temperature_min = temperature_min[new_column_order]
    
    return temperature_min

def load_evapotranspiration_data(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    evapotranspiration_data = pd.concat(dataframes, ignore_index=True)
    evapotranspiration_cleaned = evapotranspiration_data.copy()
    evapotranspiration_cleaned = evapotranspiration_cleaned.dropna()
    evapotranspiration = evapotranspiration_cleaned.drop('น้ำระเหยถาด(มิลลิเมตร)', axis=1)
    
    evapotranspiration.rename(
        columns={**{
            f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
        },
        "Unnamed: 1": "station",
        "Unnamed: 2": "datetime",
        "Unnamed: 34": "evapotranspiration"},
        inplace=True
    )
    
    evapotranspiration['datetime'] = pd.to_datetime(evapotranspiration['datetime'], format='%b-%y')
    evapotranspiration['datetime'] = pd.to_datetime(evapotranspiration['datetime'], format='%d-%m-%Y')
    evapotranspiration['year'] = evapotranspiration['datetime'].dt.year
    evapotranspiration['month'] = evapotranspiration['datetime'].dt.month
    
    new_column_order = ['station', 'datetime', 'year', 'month'] + \
                       [f'day{i}' for i in range(1, 32)] + ['evapotranspiration']
    evapotranspiration = evapotranspiration[new_column_order]
    
    return evapotranspiration

def preprocess_all_data(humidity_paths, rainfall_paths, temperature_max_paths, temperature_min_paths, evapotranspiration_paths):
    humidity_data = load_humidity_data(humidity_paths)
    rainfall_data = load_rainfall_data(rainfall_paths)
    temperature_max_data = load_temperature_max_data(temperature_max_paths)
    temperature_min_data = load_temperature_min_data(temperature_min_paths)
    evapotranspiration_data = load_evapotranspiration_data(evapotranspiration_paths)
    
    return humidity_data, rainfall_data, temperature_max_data, temperature_min_data, evapotranspiration_data