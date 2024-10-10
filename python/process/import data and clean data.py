# นี่คือขั้นตอนทำความสะอาดชุดข้อมูล
# นี่ตือชุดข้อมูล Humidity ( ความชื้นสัมพัทธ์ )
## Humidity ( ความชื้นสัมพัทธ์ )

humidity_data = [
    r"D:\project\Data\humid\humid-d-N-1-1998-2003.csv",
    r"D:\project\Data\humid\humid-d-N-2-1998-2003.csv",
    r"D:\project\Data\humid\humid-d-N-1-2004-2013.csv",
    r"D:\project\Data\humid\humid-d-N-2-2004-2013.csv",
    r"D:\project\Data\humid\humid-d-N-1-2014-2023.csv",
    r"D:\project\Data\humid\humid-d-N-2-2014-2023.csv"
]

dataframes = [pd.read_csv(file) for file in humidity_data]
humidity_data = pd.concat(dataframes, ignore_index=True)

# สร้างสำเนาของ DataFrame
humidity_cleaned = humidity_data.copy()
humidity_cleaned

humidity_cleaned.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
humidity_cleaned.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = humidity_cleaned.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(humidity_cleaned)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

humidity = humidity_cleaned.dropna()
humidity

humidity = humidity.drop('ความชื้นสัมพัทธ์(เปอร์เซ็นต์)', axis=1)
humidity

humidity.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
humidity.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = humidity.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(humidity)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

humidity.rename(
    columns={**{
        f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
    },
    "Unnamed: 1": "station",
    "Unnamed: 2": "datetime",
    "Unnamed: 34": "humidity"},
    inplace=True
)
humidity

humidity['datetime'] = pd.to_datetime(humidity['datetime'], format='%b-%y')
humidity

humidity['datetime'] = pd.to_datetime(humidity['datetime'], format='%d-%m-%Y')
humidity['year'] = humidity['datetime'].dt.year
humidity['month'] = humidity['datetime'].dt.month
humidity

new_column_order = ['station', 'datetime', 'year', 'month'] + \
                   [f'day{i}' for i in range(1, 32)] + ['humidity']

humidity = humidity[new_column_order]
humidity

# นี่ตือชุดข้อมูล Rainfall ( ปริมาณน้ำฝน )
## Rainfall ( ปริมาณน้ำฝน )

rainfall_data = [
    r"D:\project\Data\Rain\Rain-N1-2003-1998.csv",
    r"D:\project\Data\Rain\Rain-N2-2003-1998.csv",
    r"D:\project\Data\Rain\Rain-N1-2013-2004.csv",
    r"D:\project\Data\Rain\Rain-N2-2013-2004.csv",
    r"D:\project\Data\Rain\Rain-N1-2023-2014.csv",
    r"D:\project\Data\Rain\Rain-N2-2023-2014.csv"
]

dataframes= [pd.read_csv(file) for file in rainfall_data]
rainfall_data = pd.concat(dataframes, ignore_index=True)

# สร้างสำเนาของ DataFrame
rainfall_cleaned = rainfall_data.copy()
rainfall_cleaned

rainfall_cleaned.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
rainfall_cleaned.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = rainfall_cleaned.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(rainfall_cleaned)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

rainfall = rainfall_cleaned.dropna()
rainfall

rainfall = rainfall.drop('ปริมาณฝน(มิลลิเมตร)', axis=1)
rainfall

rainfall.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
rainfall.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = rainfall.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(rainfall)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

rainfall.rename(
    columns={**{
        f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
    },
    "Unnamed: 1": "station",
    "Unnamed: 2": "datetime",
    "Unnamed: 34": "rainfall"},
    inplace=True
)
rainfall

rainfall['datetime'] = pd.to_datetime(rainfall['datetime'], format='%b-%y')
rainfall

rainfall['datetime'] = pd.to_datetime(rainfall['datetime'], format='%d-%m-%Y')
rainfall['year'] = rainfall['datetime'].dt.year
rainfall['month'] = rainfall['datetime'].dt.month
rainfall

new_column_order = ['station', 'datetime', 'year', 'month'] + \
                   [f'day{i}' for i in range(1, 32)] + ['rainfall']

rainfall = rainfall[new_column_order]
rainfall

# นี่ตือชุดข้อมูล Temperature max ( อุณหภูมิสูงสุด )
## Temperature max ( อุณหภูมิสูงสุด )

temperature_max_data = [
    r"D:\project\Data\MaxT\MaxT-N1-2003-1998.csv",
    r"D:\project\Data\MaxT\MaxT-N2-2003-1998.csv",
    r"D:\project\Data\MaxT\MaxT-N1-2013-2004.csv",
    r"D:\project\Data\MaxT\MaxT-N2-2013-2004.csv",
    r"D:\project\Data\MaxT\MaxT-N1-2023-2014.csv",
    r"D:\project\Data\MaxT\MaxT-N2-2023-2014.csv"
]

dataframes= [pd.read_csv(file) for file in temperature_max_data]
temperature_max_data = pd.concat(dataframes, ignore_index=True)

# สร้างสำเนาของ DataFrame
temperature_max_cleaned = temperature_max_data.copy()
temperature_max_cleaned

temperature_max_cleaned.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
temperature_max_cleaned.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = temperature_max_cleaned.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(temperature_max_cleaned)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

temperature_max = temperature_max_cleaned.dropna()
temperature_max

temperature_max = temperature_max.drop('อุณหภูมิสูงสุด(เซลเซียส)', axis=1)
temperature_max

temperature_max.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
rainfall.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = temperature_max.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(temperature_max)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

temperature_max.rename(
    columns={**{
        f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
    },
    "Unnamed: 1": "station",
    "Unnamed: 2": "datetime",
    "Unnamed: 34": "temperature_max"},
    inplace=True
)
temperature_max

temperature_max['datetime'] = pd.to_datetime(temperature_max['datetime'], format='%b-%y')
temperature_max

temperature_max['datetime'] = pd.to_datetime(temperature_max['datetime'], format='%d-%m-%Y')
temperature_max['year'] = temperature_max['datetime'].dt.year
temperature_max['month'] = temperature_max['datetime'].dt.month
temperature_max

new_column_order = ['station', 'datetime', 'year', 'month'] + \
                   [f'day{i}' for i in range(1, 32)] + ['temperature_max']

temperature_max = temperature_max[new_column_order]
temperature_max

# นี่คือชุดข้อมูล Temperature min ( อุณหภูมิต่ำสุด )
## Temperature min ( อุณหภูมิต่ำสุด )

temperature_min_data = [
    r"D:\project\Data\MinT\MinT-N1-2003-1998.csv",
    r"D:\project\Data\MinT\MinT-N2-2003-1998.csv",
    r"D:\project\Data\MinT\MinT-N1-2013-2004.csv",
    r"D:\project\Data\MinT\MinT-N2-2013-2004.csv",
    r"D:\project\Data\MinT\MinT-N1-2023-2014.csv",
    r"D:\project\Data\MinT\MinT-N2-2023-2014.csv"
]

dataframes= [pd.read_csv(file) for file in temperature_min_data]
temperature_min_data = pd.concat(dataframes, ignore_index=True)

# สร้างสำเนาของ DataFrame
temperature_min_cleaned = temperature_min_data.copy()
temperature_min_cleaned

temperature_min_cleaned.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
temperature_min_cleaned.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = temperature_min_cleaned.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(temperature_min_cleaned)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

temperature_min = temperature_min_cleaned.dropna()
temperature_min

temperature_min = temperature_min.drop('อุณหภูมิต่ำสุด(เซลเซียส)', axis=1)
temperature_min

temperature_min.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
temperature_min.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = temperature_min.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(temperature_min)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

temperature_min.rename(
    columns={**{
        f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
    },
    "Unnamed: 1": "station",
    "Unnamed: 2": "datetime",
    "Unnamed: 34": "temperature_min"},
    inplace=True
)
temperature_min

temperature_min['datetime'] = pd.to_datetime(temperature_min['datetime'], format='%b-%y')
temperature_min

temperature_min['datetime'] = pd.to_datetime(temperature_min['datetime'], format='%d-%m-%Y')
temperature_min['year'] = temperature_min['datetime'].dt.year
temperature_min['month'] = temperature_min['datetime'].dt.month
temperature_min

new_column_order = ['station', 'datetime', 'year', 'month'] + \
                   [f'day{i}' for i in range(1, 32)] + ['temperature_min']

temperature_min = temperature_min[new_column_order]
temperature_min

# นี่คือชุดข้อมูล Evapotranspiration ( น้ำระเหยถาด )
## Evapotranspiration ( น้ำระเหยถาด )

evapotranspiration_data = [
    r"D:\project\Data\eva\eva-d-N-1-1998-2003.csv",
    r"D:\project\Data\eva\eva-d-N-2-1998-2003.csv",
    r"D:\project\Data\eva\eva-d-N-1-2004-2013.csv",
    r"D:\project\Data\eva\eva-d-N-2-2004-2013.csv",
    r"D:\project\Data\eva\eva-d-N-1-2014-2023.csv",
    r"D:\project\Data\eva\eva-d-N-2-2014-2023.csv"
]

dataframes= [pd.read_csv(file) for file in evapotranspiration_data]
evapotranspiration_data = pd.concat(dataframes, ignore_index=True)

# สร้างสำเนาของ DataFrame
evapotranspiration_cleaned = evapotranspiration_data.copy()
evapotranspiration_cleaned

evapotranspiration_cleaned.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
evapotranspiration_cleaned.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = evapotranspiration_cleaned.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(evapotranspiration_cleaned)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

evapotranspiration = evapotranspiration_cleaned.dropna()
evapotranspiration

evapotranspiration = evapotranspiration.drop('น้ำระเหยถาด(มิลลิเมตร)', axis=1)
evapotranspiration

evapotranspiration.shape

print("ข้อมูลเบื้องต้นของ DataFrame:")
evapotranspiration.info()

print("จำนวนค่าที่หายไปในแต่ละคอลัมน์:")
missing_values = evapotranspiration.isnull().sum()
missing_values[missing_values > 0]

missing_percentage = (missing_values / len(evapotranspiration)) * 100
print("สัดส่วนของข้อมูลที่หายไปในแต่ละคอลัมน์ (%):")
missing_percentage[missing_percentage > 0]

evapotranspiration.rename(
    columns={**{
        f"Unnamed: {i}": f"day{i-2}".lower() for i in range(3, 34)
    },
    "Unnamed: 1": "station",
    "Unnamed: 2": "datetime",
    "Unnamed: 34": "evapotranspiration"},
    inplace=True
)
evapotranspiration

evapotranspiration['datetime'] = pd.to_datetime(evapotranspiration['datetime'], format='%b-%y')
evapotranspiration

evapotranspiration['datetime'] = pd.to_datetime(evapotranspiration['datetime'], format='%d-%m-%Y')
evapotranspiration['year'] = evapotranspiration['datetime'].dt.year
evapotranspiration['month'] = evapotranspiration['datetime'].dt.month
evapotranspiration

new_column_order = ['station', 'datetime', 'year', 'month'] + \
                   [f'day{i}' for i in range(1, 32)] + ['evapotranspiration']

evapotranspiration = evapotranspiration[new_column_order]
evapotranspiration