# clean Rain
import pandas as pd

# List of file paths (make sure these match the uploaded files)
rainfall_files = [
    '/content/Rain-N1-2003-1998.csv',
    '/content/Rain-N1-2013-2004.csv',
    '/content/Rain-N1-2023-2014.csv',
    '/content/Rain-N2-2003-1998.csv',
    '/content/Rain-N2-2013-2004.csv',
    '/content/Rain-N2-2023-2014.csv'
]

# Create an empty DataFrame to store the concatenated data
rainfall_data = pd.DataFrame()

# Iterate over the file paths and concatenate the DataFrames
for file_path in rainfall_files:
    temp_df = pd.read_csv(file_path)  # Read each CSV file
    rainfall_data = pd.concat([rainfall_data, temp_df], ignore_index=True)  # Concatenate to the main DataFrame

# Display the first 10 rows of the concatenated DataFrame
rainfall_data.head(10)


# ตรวจสอบค่าว่างใน DataFrame
null_values = rainfall_data.isnull()

# แสดงผลลัพธ์การตรวจสอบค่าที่หายไป
null_values.head(10) # แสดง 10 แถวแรก

# นับจำนวนค่าที่หายไปในแต่ละคอลัมน์และแสดงผลลัพธ์
print(rainfall_data.isnull().sum())

# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_rainfall_data = rainfall_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_rainfall_data.head(10)

# แสดงขนาดของ DataFrame ใหม่
cleaned_rainfall_data.shape

# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_rainfall_data = rainfall_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_rainfall_data.head(10)

cleaned_rainfall_data.tail(10)
cleaned_rainfall_data.shape
cleaned_rainfall_data.isnull()
# ตรวจสอบจำนวนค่าที่หายไปในแต่ละคอลัมน์ของ DataFrame ที่ทำความสะอาดแล้ว
missing_values_summary = cleaned_rainfall_data.isnull().sum()

# แสดงผลลัพธ์ของจำนวนค่าที่หายไปในแต่ละคอลัมน์
print(missing_values_summary)
# เปลี่ยนชื่อคอลัมน์ใน DataFrame
cleaned_rainfall_data.rename(
    columns={
        "ปริมาณฝน(มิลลิเมตร)": "NO",
        "Unnamed: 1": "STATION",
        "Unnamed: 2": "Datetime",
        "Unnamed: 3": "Day1",
        "Unnamed: 4": "Day2",
        "Unnamed: 5": "Day3",
        "Unnamed: 6": "Day4",
        "Unnamed: 7": "Day5",
        "Unnamed: 8": "Day6",
        "Unnamed: 9": "Day7",
        "Unnamed: 10": "Day8",
        "Unnamed: 11": "Day9",
        "Unnamed: 12": "Day10",
        "Unnamed: 13": "Day11",
        "Unnamed: 14": "Day12",
        "Unnamed: 15": "Day13",
        "Unnamed: 16": "Day14",
        "Unnamed: 17": "Day15",
        "Unnamed: 18": "Day16",
        "Unnamed: 19": "Day17",
        "Unnamed: 20": "Day18",
        "Unnamed: 21": "Day19",
        "Unnamed: 22": "Day20",
        "Unnamed: 23": "Day21",
        "Unnamed: 24": "Day22",
        "Unnamed: 25": "Day23",
        "Unnamed: 26": "Day24",
        "Unnamed: 27": "Day25",
        "Unnamed: 28": "Day26",
        "Unnamed: 29": "Day27",
        "Unnamed: 30": "Day28",
        "Unnamed: 31": "Day29",
        "Unnamed: 32": "Day30",
        "Unnamed: 33": "Day31",
        "Unnamed: 34": "Rainfall"
    },
    inplace=True
)

# แสดง DataFrame หลังจากเปลี่ยนชื่อคอลัมน์
cleaned_rainfall_data

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_rainfall_data['Datetime'] = pd.to_datetime(cleaned_rainfall_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_rainfall_data['Year'] = cleaned_rainfall_data['Datetime'].dt.year
cleaned_rainfall_data['Month'] = cleaned_rainfall_data['Datetime'].dt.month

# ตรวจสอบปีที่หายไปในแต่ละสถานี
missing_years_list = []
for station in cleaned_rainfall_data['STATION'].unique():
    # สร้างชุดปีทั้งหมดที่มีในข้อมูล
    all_years = set(cleaned_rainfall_data['Year'])
    years_with_data = set(cleaned_rainfall_data[cleaned_rainfall_data['STATION'] == station]['Year'])
    missing_years_in_station = all_years - years_with_data

    # ตรวจสอบเดือนที่หายไปในแต่ละปีที่มีข้อมูล
    for year in missing_years_in_station:
        missing_years_list.append({
            'STATION': station,
            'Year': year,
            'Missing Months': 'All months missing'
        })

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = cleaned_rainfall_data[(cleaned_rainfall_data['STATION'] == station) & (cleaned_rainfall_data['Year'] == year)]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        if missing_months:
            missing_years_list.append({
                'STATION': station,
                'Year': year,
                'Missing Months': sorted(missing_months)
            })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_years_df = pd.DataFrame(missing_years_list)

# แสดงข้อมูลที่หายไป
if not missing_years_df.empty:
    print("มีสถานีที่มีข้อมูลปีและเดือนหายไป:")
    print(missing_years_df)
else:
    print("ทุกสถานีมีข้อมูลปีและเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_rainfall_data['Datetime'] = pd.to_datetime(cleaned_rainfall_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_rainfall_data['Year'] = cleaned_rainfall_data['Datetime'].dt.year
cleaned_rainfall_data['Month'] = cleaned_rainfall_data['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
missing_months_summary = []

for station in cleaned_rainfall_data['STATION'].unique():
    station_data = cleaned_rainfall_data[cleaned_rainfall_data['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
    missing_percentage = (missing_months_count / total_months) * 100

    # เก็บข้อมูลผลลัพธ์
    missing_months_summary.append({
        'STATION': station,
        'Total Missing Months': missing_months_count,
        'Percentage Missing': missing_percentage
    })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_months_df = pd.DataFrame(missing_months_summary)

# แสดงข้อมูลที่หายไป
if not missing_months_df.empty:
    print("ข้อมูลเปอร์เซ็นต์ของเดือนที่หายไปสำหรับแต่ละสถานี:")
    print(missing_months_df)
else:
    print("ทุกสถานีมีข้อมูลเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_rainfall_data['Datetime'] = pd.to_datetime(cleaned_rainfall_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_rainfall_data['Year'] = cleaned_rainfall_data['Datetime'].dt.year
cleaned_rainfall_data['Month'] = cleaned_rainfall_data['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
total_months_all_stations = 0
missing_months_all_stations = 0

for station in cleaned_rainfall_data['STATION'].unique():
    station_data = cleaned_rainfall_data[cleaned_rainfall_data['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # อัปเดตค่าทั้งหมดสำหรับทุกสถานี
    total_months_all_stations += total_months
    missing_months_all_stations += missing_months_count

# คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
missing_percentage_all_stations = (missing_months_all_stations / total_months_all_stations) * 100

# แสดงผลลัพธ์
print(f"รวมข้อมูลสำหรับทุกสถานีในช่วงปี {start_year}-{end_year}:")
print(f"จำนวนเดือนทั้งหมดที่คาดหวัง: {total_months_all_stations}")
print(f"จำนวนเดือนที่หายไป: {missing_months_all_stations}")
print(f"เปอร์เซ็นต์ของเดือนที่หายไป: {missing_percentage_all_stations:.2f}%")

# เปลี่ยนคอลัมน์ 'Datetime' ใน cleaned_rainfall_data เป็นประเภทวันที่
cleaned_rainfall_data['Datetime'] = pd.to_datetime(cleaned_rainfall_data['Datetime'], format='%b-%y')

# แสดง 10 แถวแรกของ DataFrame
cleaned_rainfall_data.head(10)

# สร้างคอลัมน์ 'YEAR' จากคอลัมน์ 'Datetime'
cleaned_rainfall_data['YEAR'] = cleaned_rainfall_data['Datetime'].dt.year

# แสดง 10 แถวแรกของ DataFrame
cleaned_rainfall_data.head(10)

# เปลี่ยนชื่อคอลัมน์เป็นตัวพิมพ์ใหญ่
cleaned_rainfall_data.columns = [col.upper() for col in cleaned_rainfall_data.columns]

# กำหนดชื่อคอลัมน์ใหม่ (ตัวพิมพ์ใหญ่)
new_columns = [
    'NO', 'STATION', 'DATETIME',
    'DAY1', 'DAY2', 'DAY3', 'DAY4', 'DAY5', 'DAY6', 'DAY7', 'DAY8', 'DAY9',
    'DAY10', 'DAY11', 'DAY12', 'DAY13', 'DAY14', 'DAY15', 'DAY16', 'DAY17',
    'DAY18', 'DAY19', 'DAY20', 'DAY21', 'DAY22', 'DAY23', 'DAY24', 'DAY25',
    'DAY26', 'DAY27', 'DAY28', 'DAY29', 'DAY30', 'DAY31', 'RAINFALL'
]

# เลือกเฉพาะคอลัมน์ที่ต้องการใน DataFrame
cleaned_rainfall_data = cleaned_rainfall_data[new_columns]

# แสดง 10 แถวแรกของ DataFrame
cleaned_rainfall_data.head(10)
cleaned_rainfall_data.shape
cleaned_rainfall_data['NO'] = range(1, len(cleaned_rainfall_data) + 1)
cleaned_rainfall_data.head(10)
import pandas as pd

columns_to_drop = [f'DAY{i}' for i in range(1, 32)] + ['NO']

# ลบคอลัมน์ที่ระบุจาก DataFrame cleaned_rainfall_data
cleaned_rainfall_data = cleaned_rainfall_data.drop(columns=columns_to_drop)

# รีเซ็ตดัชนีของ DataFrame
cleaned_rainfall_data = cleaned_rainfall_data.reset_index(drop=True)

# ตรวจสอบผลลัพธ์
print(cleaned_rainfall_data)

# clean Evaporation
import pandas as pd

# List of file paths (make sure these match the uploaded files)
file_paths = [
    '/content/eva-d-N-1-1998-2003.csv',
    '/content/eva-d-N-1-2004-2013.csv',
    '/content/eva-d-N-1-2014-2023.csv',
    '/content/eva-d-N-2-1998-2003.csv',
    '/content/eva-d-N-2-2004-2013.csv',
    '/content/eva-d-N-2-2014-2023.csv'
]

# Create an empty DataFrame to store the concatenated data
evaporation_data = pd.DataFrame()

# Iterate over the file paths and concatenate the DataFrames
for file_path in file_paths:
    temp_df = pd.read_csv(file_path)  # Read each CSV file
    evaporation_data = pd.concat([evaporation_data, temp_df], ignore_index=True)  # Concatenate to the main DataFrame

# Display the first 10 rows of the concatenated DataFrame
evaporation_data.head(10)


# ตรวจสอบค่าว่างใน DataFrame
null_values = evaporation_data.isnull()

# แสดงผลลัพธ์การตรวจสอบค่าที่หายไป
null_values.head(10)
# นับจำนวนค่าที่หายไปในแต่ละคอลัมน์และแสดงผลลัพธ์
print(evaporation_data.isnull().sum())
# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_evaporation_data = evaporation_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_evaporation_data.head(10)

# แสดงขนาดของ DataFrame ใหม่
cleaned_evaporation_data.shape

# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_evaporation_data = evaporation_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_evaporation_data.head(10)

cleaned_evaporation_data.tail(10)
cleaned_evaporation_data.shape
cleaned_evaporation_data.isnull()
# ตรวจสอบจำนวนค่าที่หายไปในแต่ละคอลัมน์ของ DataFrame ที่ทำความสะอาดแล้ว
missing_values_summary = cleaned_evaporation_data.isnull().sum()

# แสดงผลลัพธ์ของจำนวนค่าที่หายไปในแต่ละคอลัมน์
print(missing_values_summary)
# เปลี่ยนชื่อคอลัมน์ใน DataFrame
cleaned_evaporation_data.rename(
    columns={
        "ปริมาณฝน(มิลลิเมตร)": "NO",
        "Unnamed: 1": "STATION",
        "Unnamed: 2": "Datetime",
        "Unnamed: 3": "Day1",
        "Unnamed: 4": "Day2",
        "Unnamed: 5": "Day3",
        "Unnamed: 6": "Day4",
        "Unnamed: 7": "Day5",
        "Unnamed: 8": "Day6",
        "Unnamed: 9": "Day7",
        "Unnamed: 10": "Day8",
        "Unnamed: 11": "Day9",
        "Unnamed: 12": "Day10",
        "Unnamed: 13": "Day11",
        "Unnamed: 14": "Day12",
        "Unnamed: 15": "Day13",
        "Unnamed: 16": "Day14",
        "Unnamed: 17": "Day15",
        "Unnamed: 18": "Day16",
        "Unnamed: 19": "Day17",
        "Unnamed: 20": "Day18",
        "Unnamed: 21": "Day19",
        "Unnamed: 22": "Day20",
        "Unnamed: 23": "Day21",
        "Unnamed: 24": "Day22",
        "Unnamed: 25": "Day23",
        "Unnamed: 26": "Day24",
        "Unnamed: 27": "Day25",
        "Unnamed: 28": "Day26",
        "Unnamed: 29": "Day27",
        "Unnamed: 30": "Day28",
        "Unnamed: 31": "Day29",
        "Unnamed: 32": "Day30",
        "Unnamed: 33": "Day31",
        "Unnamed: 34": "Evaporation"
    },
    inplace=True
)

# แสดง DataFrame หลังจากเปลี่ยนชื่อคอลัมน์
cleaned_evaporation_data

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_evaporation_data['Datetime'] = pd.to_datetime(cleaned_evaporation_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_evaporation_data['Year'] = cleaned_evaporation_data['Datetime'].dt.year
cleaned_evaporation_data['Month'] = cleaned_evaporation_data['Datetime'].dt.month

# ตรวจสอบปีที่หายไปในแต่ละสถานี
missing_years_list = []
for station in cleaned_evaporation_data['STATION'].unique():
    # สร้างชุดปีทั้งหมดที่มีในข้อมูล
    all_years = set(cleaned_evaporation_data['Year'])
    years_with_data = set(cleaned_evaporation_data[cleaned_evaporation_data['STATION'] == station]['Year'])
    missing_years_in_station = all_years - years_with_data

    # ตรวจสอบเดือนที่หายไปในแต่ละปีที่มีข้อมูล
    for year in missing_years_in_station:
        missing_years_list.append({
            'STATION': station,
            'Year': year,
            'Missing Months': 'All months missing'
        })

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = cleaned_evaporation_data[(cleaned_evaporation_data['STATION'] == station) & (cleaned_evaporation_data['Year'] == year)]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        if missing_months:
            missing_years_list.append({
                'STATION': station,
                'Year': year,
                'Missing Months': sorted(missing_months)
            })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_years_df = pd.DataFrame(missing_years_list)

# แสดงข้อมูลที่หายไป
if not missing_years_df.empty:
    print("มีสถานีที่มีข้อมูลปีและเดือนหายไป:")
    print(missing_years_df)
else:
    print("ทุกสถานีมีข้อมูลปีและเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_evaporation_data['Datetime'] = pd.to_datetime(cleaned_evaporation_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_evaporation_data['Year'] = cleaned_evaporation_data['Datetime'].dt.year
cleaned_evaporation_data['Month'] = cleaned_evaporation_data['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
missing_months_summary = []

for station in cleaned_evaporation_data['STATION'].unique():
    station_data = cleaned_evaporation_data[cleaned_evaporation_data['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
    missing_percentage = (missing_months_count / total_months) * 100

    # เก็บข้อมูลผลลัพธ์
    missing_months_summary.append({
        'STATION': station,
        'Total Missing Months': missing_months_count,
        'Percentage Missing': missing_percentage
    })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_months_df = pd.DataFrame(missing_months_summary)

# แสดงข้อมูลที่หายไป
if not missing_months_df.empty:
    print("ข้อมูลเปอร์เซ็นต์ของเดือนที่หายไปสำหรับแต่ละสถานี:")
    print(missing_months_df)
else:
    print("ทุกสถานีมีข้อมูลเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_evaporation_data['Datetime'] = pd.to_datetime(cleaned_evaporation_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_evaporation_data['Year'] = cleaned_evaporation_data['Datetime'].dt.year
cleaned_evaporation_data['Month'] = cleaned_evaporation_data['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
total_months_all_stations = 0
missing_months_all_stations = 0

for station in cleaned_evaporation_data['STATION'].unique():
    station_data = cleaned_evaporation_data[cleaned_evaporation_data['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # อัปเดตค่าทั้งหมดสำหรับทุกสถานี
    total_months_all_stations += total_months
    missing_months_all_stations += missing_months_count

# คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
missing_percentage_all_stations = (missing_months_all_stations / total_months_all_stations) * 100

# แสดงผลลัพธ์
print(f"รวมข้อมูลสำหรับทุกสถานีในช่วงปี {start_year}-{end_year}:")
print(f"จำนวนเดือนทั้งหมดที่คาดหวัง: {total_months_all_stations}")
print(f"จำนวนเดือนที่หายไป: {missing_months_all_stations}")
print(f"เปอร์เซ็นต์ของเดือนที่หายไป: {missing_percentage_all_stations:.2f}%")

# เปลี่ยนคอลัมน์ 'Datetime' ใน cleaned_rainfall_data เป็นประเภทวันที่
cleaned_evaporation_data['Datetime'] = pd.to_datetime(cleaned_evaporation_data['Datetime'], format='%b-%y')

# แสดง 10 แถวแรกของ DataFrame
cleaned_evaporation_data.head(10)

# สร้างคอลัมน์ 'YEAR' จากคอลัมน์ 'Datetime'
cleaned_evaporation_data['YEAR'] = cleaned_evaporation_data['Datetime'].dt.year

# แสดง 10 แถวแรกของ DataFrame
cleaned_evaporation_data.head(10)

# เปลี่ยนชื่อคอลัมน์เป็นตัวพิมพ์ใหญ่
cleaned_evaporation_data.columns = [col.upper() for col in cleaned_evaporation_data.columns]

# กำหนดชื่อคอลัมน์ใหม่ (ตัวพิมพ์ใหญ่)
new_columns = [
    'STATION', 'DATETIME',
    'DAY1', 'DAY2', 'DAY3', 'DAY4', 'DAY5', 'DAY6', 'DAY7', 'DAY8', 'DAY9',
    'DAY10', 'DAY11', 'DAY12', 'DAY13', 'DAY14', 'DAY15', 'DAY16', 'DAY17',
    'DAY18', 'DAY19', 'DAY20', 'DAY21', 'DAY22', 'DAY23', 'DAY24', 'DAY25',
    'DAY26', 'DAY27', 'DAY28', 'DAY29', 'DAY30', 'DAY31', 'EVAPORATION'
]

# เลือกเฉพาะคอลัมน์ที่ต้องการใน DataFrame
cleaned_evaporation_data = cleaned_evaporation_data[new_columns]

# สร้างคอลัมน์ 'NO' และเพิ่ม "NO" ในทุกแถว
cleaned_evaporation_data['NO'] = 'NO'

# จัดเรียงคอลัมน์ใหม่ให้อยู่ในลำดับที่ต้องการ
cleaned_evaporation_data = cleaned_evaporation_data[['NO'] + new_columns]

# แสดง 10 แถวแรกของ DataFrame
cleaned_evaporation_data.head(10)
cleaned_evaporation_data.shape
cleaned_evaporation_data['NO'] = range(1, len(cleaned_evaporation_data) + 1)
cleaned_evaporation_data.head(10)
import pandas as pd

columns_to_drop = [f'DAY{i}' for i in range(1, 32)] + ['NO']

# ลบคอลัมน์ที่ระบุจาก DataFrame cleaned_rainfall_data
cleaned_evaporation_data = cleaned_evaporation_data.drop(columns=columns_to_drop)

# รีเซ็ตดัชนีของ DataFrame
cleaned_evaporation_data = cleaned_evaporation_data.reset_index(drop=True)

# ตรวจสอบผลลัพธ์
print(cleaned_evaporation_data)

# clean Rain Tem low hight
## TEMhigh
import pandas as pd

# List of file paths (make sure these match the uploaded files)
temperature_files = [
    '/content/MaxT-N1-2003-1998.csv',
    '/content/MaxT-N1-2013-2004.csv',
    '/content/MaxT-N1-2023-2014.csv',
    '/content/MaxT-N2-2003-1998.csv',
    '/content/MaxT-N2-2013-2004.csv',
    '/content/MaxT-N2-2023-2014.csv'
]

# Create an empty DataFrame to store the concatenated data
temperature_data = pd.DataFrame()

# Iterate over the file paths and concatenate the DataFrames
for file_path in temperature_files:
    temp_df = pd.read_csv(file_path)  # Read each CSV file
    temperature_data = pd.concat([temperature_data, temp_df], ignore_index=True)  # Concatenate to the main DataFrame

# Display the first 10 rows of the concatenated DataFrame
temperature_data.head(10)

# ตรวจสอบค่าว่างใน DataFrame
null_values = temperature_data.isnull()

# แสดงผลลัพธ์การตรวจสอบค่าที่หายไป
null_values.head(10)  # แสดง 10 แถวแรก

# นับจำนวนค่าที่หายไปในแต่ละคอลัมน์และแสดงผลลัพธ์
print(temperature_data.isnull().sum())

# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_temperature_data = temperature_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_temperature_data.head(10)

# แสดงขนาดของ DataFrame ใหม่
cleaned_temperature_data.shape

# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_temperature_data = temperature_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_temperature_data.head(10)

cleaned_temperature_data.tail(10)
cleaned_temperature_data.shape
cleaned_temperature_data.isnull()
# ตรวจสอบจำนวนค่าที่หายไปในแต่ละคอลัมน์ของ DataFrame ที่ทำความสะอาดแล้ว
missing_values_summary = cleaned_temperature_data.isnull().sum()

# แสดงผลลัพธ์ของจำนวนค่าที่หายไปในแต่ละคอลัมน์
print(missing_values_summary)
# เปลี่ยนชื่อคอลัมน์ใน DataFrame
cleaned_temperature_data.rename(
    columns={
        "ปริมาณฝน(มิลลิเมตร)": "NO",
        "Unnamed: 1": "STATION",
        "Unnamed: 2": "Datetime",
        "Unnamed: 3": "Day1",
        "Unnamed: 4": "Day2",
        "Unnamed: 5": "Day3",
        "Unnamed: 6": "Day4",
        "Unnamed: 7": "Day5",
        "Unnamed: 8": "Day6",
        "Unnamed: 9": "Day7",
        "Unnamed: 10": "Day8",
        "Unnamed: 11": "Day9",
        "Unnamed: 12": "Day10",
        "Unnamed: 13": "Day11",
        "Unnamed: 14": "Day12",
        "Unnamed: 15": "Day13",
        "Unnamed: 16": "Day14",
        "Unnamed: 17": "Day15",
        "Unnamed: 18": "Day16",
        "Unnamed: 19": "Day17",
        "Unnamed: 20": "Day18",
        "Unnamed: 21": "Day19",
        "Unnamed: 22": "Day20",
        "Unnamed: 23": "Day21",
        "Unnamed: 24": "Day22",
        "Unnamed: 25": "Day23",
        "Unnamed: 26": "Day24",
        "Unnamed: 27": "Day25",
        "Unnamed: 28": "Day26",
        "Unnamed: 29": "Day27",
        "Unnamed: 30": "Day28",
        "Unnamed: 31": "Day29",
        "Unnamed: 32": "Day30",
        "Unnamed: 33": "Day31",
        "Unnamed: 34": "average"
    },
    inplace=True
)

# แสดง DataFrame หลังจากเปลี่ยนชื่อคอลัมน์
cleaned_temperature_data

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_temperature_data['Datetime'] = pd.to_datetime(cleaned_temperature_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_temperature_data['Year'] = cleaned_temperature_data['Datetime'].dt.year
cleaned_temperature_data['Month'] = cleaned_temperature_data['Datetime'].dt.month

# ตรวจสอบปีที่หายไปในแต่ละสถานี
missing_years_list = []
for station in cleaned_temperature_data['STATION'].unique():
    # สร้างชุดปีทั้งหมดที่มีในข้อมูล
    all_years = set(cleaned_temperature_data['Year'])
    years_with_data = set(cleaned_temperature_data[cleaned_temperature_data['STATION'] == station]['Year'])
    missing_years_in_station = all_years - years_with_data

    # ตรวจสอบเดือนที่หายไปในแต่ละปีที่มีข้อมูล
    for year in missing_years_in_station:
        missing_years_list.append({
            'STATION': station,
            'Year': year,
            'Missing Months': 'All months missing'
        })

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = cleaned_temperature_data[(cleaned_temperature_data['STATION'] == station) & (cleaned_temperature_data['Year'] == year)]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        if missing_months:
            missing_years_list.append({
                'STATION': station,
                'Year': year,
                'Missing Months': sorted(missing_months)
            })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_years_df = pd.DataFrame(missing_years_list)

# แสดงข้อมูลที่หายไป
if not missing_years_df.empty:
    print("มีสถานีที่มีข้อมูลปีและเดือนหายไป:")
    print(missing_years_df)
else:
    print("ทุกสถานีมีข้อมูลปีและเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_temperature_data['Datetime'] = pd.to_datetime(cleaned_temperature_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_temperature_data['Year'] = cleaned_temperature_data['Datetime'].dt.year
cleaned_temperature_data['Month'] = cleaned_temperature_data['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
missing_months_summary = []

for station in cleaned_temperature_data['STATION'].unique():
    station_data = cleaned_temperature_data[cleaned_temperature_data['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
    missing_percentage = (missing_months_count / total_months) * 100

    # เก็บข้อมูลผลลัพธ์
    missing_months_summary.append({
        'STATION': station,
        'Total Missing Months': missing_months_count,
        'Percentage Missing': missing_percentage
    })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_months_df = pd.DataFrame(missing_months_summary)

# แสดงข้อมูลที่หายไป
if not missing_months_df.empty:
    print("ข้อมูลเปอร์เซ็นต์ของเดือนที่หายไปสำหรับแต่ละสถานี:")
    print(missing_months_df)
else:
    print("ทุกสถานีมีข้อมูลเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_temperature_data['Datetime'] = pd.to_datetime(cleaned_temperature_data['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_temperature_data['Year'] = cleaned_temperature_data['Datetime'].dt.year
cleaned_temperature_data['Month'] = cleaned_temperature_data['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
total_months_all_stations = 0
missing_months_all_stations = 0

for station in cleaned_temperature_data['STATION'].unique():
    station_data = cleaned_temperature_data[cleaned_temperature_data['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # อัปเดตค่าทั้งหมดสำหรับทุกสถานี
    total_months_all_stations += total_months
    missing_months_all_stations += missing_months_count

# คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
missing_percentage_all_stations = (missing_months_all_stations / total_months_all_stations) * 100

# แสดงผลลัพธ์
print(f"รวมข้อมูลสำหรับทุกสถานีในช่วงปี {start_year}-{end_year}:")
print(f"จำนวนเดือนทั้งหมดที่คาดหวัง: {total_months_all_stations}")
print(f"จำนวนเดือนที่หายไป: {missing_months_all_stations}")
print(f"เปอร์เซ็นต์ของเดือนที่หายไป: {missing_percentage_all_stations:.2f}%")

# เปลี่ยนคอลัมน์ 'Datetime' ใน cleaned_rainfall_data เป็นประเภทวันที่
cleaned_temperature_data['Datetime'] = pd.to_datetime(cleaned_temperature_data['Datetime'], format='%b-%y')

# แสดง 10 แถวแรกของ DataFrame
cleaned_temperature_data.head(10)

# สร้างคอลัมน์ 'YEAR' จากคอลัมน์ 'Datetime'
cleaned_temperature_data['YEAR'] = cleaned_temperature_data['Datetime'].dt.year

# แสดง 10 แถวแรกของ DataFrame
cleaned_temperature_data.head(10)

# เปลี่ยนชื่อคอลัมน์เป็นตัวพิมพ์ใหญ่
cleaned_temperature_data.columns = [col.upper() for col in cleaned_temperature_data.columns]

# กำหนดชื่อคอลัมน์ใหม่ (ตัวพิมพ์ใหญ่)
new_columns = [
    'STATION', 'DATETIME',
    'DAY1', 'DAY2', 'DAY3', 'DAY4', 'DAY5', 'DAY6', 'DAY7', 'DAY8', 'DAY9',
    'DAY10', 'DAY11', 'DAY12', 'DAY13', 'DAY14', 'DAY15', 'DAY16', 'DAY17',
    'DAY18', 'DAY19', 'DAY20', 'DAY21', 'DAY22', 'DAY23', 'DAY24', 'DAY25',
    'DAY26', 'DAY27', 'DAY28', 'DAY29', 'DAY30', 'DAY31', 'AVERAGE'
]

# เลือกเฉพาะคอลัมน์ที่ต้องการใน DataFrame
cleaned_temperature_data = cleaned_temperature_data[new_columns]

# สร้างคอลัมน์ 'NO' และเพิ่ม "NO" ในทุกแถว
cleaned_temperature_data['NO'] = 'NO'

# จัดเรียงคอลัมน์ใหม่ให้อยู่ในลำดับที่ต้องการ
cleaned_temperature_data = cleaned_temperature_data[['NO'] + new_columns]

# แสดง 10 แถวแรกของ DataFrame
cleaned_temperature_data.head(10)
cleaned_temperature_data.shape
cleaned_temperature_data['NO'] = range(1, len(cleaned_temperature_data) + 1)
cleaned_temperature_data.head(10)
cleaned_temperature_data.drop(columns=['NO'])
cleaned_temperature_data.shape
## TEMlow
import pandas as pd

# List of file paths (make sure these match the uploaded files)
temperature_low_files = [
    '/content/MinT-N1-2003-1998.csv',
    '/content/MinT-N1-2013-2004.csv',
    '/content/MinT-N1-2023-2014.csv',
    '/content/MinT-N2-2003-1998.csv',
    '/content/MinT-N2-2013-2004.csv',
    '/content/MinT-N2-2023-2014.csv'
]

# Create an empty DataFrame to store the concatenated data
temperature_low_data = pd.DataFrame()

# Iterate over the file paths and concatenate the DataFrames
for file_path in temperature_low_files:
    temp_df = pd.read_csv(file_path)  # Read each CSV file
    temperature_low_data = pd.concat([temperature_low_data, temp_df], ignore_index=True)  # Concatenate to the main DataFrame

# Display the first 10 rows of the concatenated DataFrame
temperature_low_data.head(10)

# ตรวจสอบค่าว่างใน DataFrame
null_values = temperature_low_data.isnull()

# แสดงผลลัพธ์การตรวจสอบค่าที่หายไป
null_values.head(10)  # แสดง 10 แถวแรก

# นับจำนวนค่าที่หายไปในแต่ละคอลัมน์และแสดงผลลัพธ์
print(temperature_low_data.isnull().sum())

# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_temperature_low = temperature_low_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_temperature_low.head(10)

# แสดงขนาดของ DataFrame ใหม่
cleaned_temperature_low.shape

# ลบแถวที่มีค่าที่หายไปและเก็บไว้ใน DataFrame ใหม่
cleaned_temperature_low = temperature_low_data.dropna()

# แสดง 10 แถวแรกของ DataFrame ใหม่
cleaned_temperature_low.head(10)

cleaned_temperature_low.tail(10)
cleaned_temperature_low.shape
cleaned_temperature_low.isnull()
# ตรวจสอบจำนวนค่าที่หายไปในแต่ละคอลัมน์ของ DataFrame ที่ทำความสะอาดแล้ว
missing_values_summary = cleaned_temperature_low.isnull().sum()

# แสดงผลลัพธ์ของจำนวนค่าที่หายไปในแต่ละคอลัมน์
print(missing_values_summary)
# เปลี่ยนชื่อคอลัมน์ใน DataFrame
cleaned_temperature_low.rename(
    columns={
        "ปริมาณฝน(มิลลิเมตร)": "NO",
        "Unnamed: 1": "STATION",
        "Unnamed: 2": "Datetime",
        "Unnamed: 3": "Day1",
        "Unnamed: 4": "Day2",
        "Unnamed: 5": "Day3",
        "Unnamed: 6": "Day4",
        "Unnamed: 7": "Day5",
        "Unnamed: 8": "Day6",
        "Unnamed: 9": "Day7",
        "Unnamed: 10": "Day8",
        "Unnamed: 11": "Day9",
        "Unnamed: 12": "Day10",
        "Unnamed: 13": "Day11",
        "Unnamed: 14": "Day12",
        "Unnamed: 15": "Day13",
        "Unnamed: 16": "Day14",
        "Unnamed: 17": "Day15",
        "Unnamed: 18": "Day16",
        "Unnamed: 19": "Day17",
        "Unnamed: 20": "Day18",
        "Unnamed: 21": "Day19",
        "Unnamed: 22": "Day20",
        "Unnamed: 23": "Day21",
        "Unnamed: 24": "Day22",
        "Unnamed: 25": "Day23",
        "Unnamed: 26": "Day24",
        "Unnamed: 27": "Day25",
        "Unnamed: 28": "Day26",
        "Unnamed: 29": "Day27",
        "Unnamed: 30": "Day28",
        "Unnamed: 31": "Day29",
        "Unnamed: 32": "Day30",
        "Unnamed: 33": "Day31",
        "Unnamed: 34": "average"
    },
    inplace=True
)

# แสดง DataFrame หลังจากเปลี่ยนชื่อคอลัมน์
cleaned_temperature_low

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_temperature_low['Datetime'] = pd.to_datetime(cleaned_temperature_low['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_temperature_low['Year'] = cleaned_temperature_low['Datetime'].dt.year
cleaned_temperature_low['Month'] = cleaned_temperature_low['Datetime'].dt.month

# ตรวจสอบปีที่หายไปในแต่ละสถานี
missing_years_list = []
for station in cleaned_temperature_low['STATION'].unique():
    # สร้างชุดปีทั้งหมดที่มีในข้อมูล
    all_years = set(cleaned_temperature_low['Year'])
    years_with_data = set(cleaned_temperature_low[cleaned_temperature_low['STATION'] == station]['Year'])
    missing_years_in_station = all_years - years_with_data

    # ตรวจสอบเดือนที่หายไปในแต่ละปีที่มีข้อมูล
    for year in missing_years_in_station:
        missing_years_list.append({
            'STATION': station,
            'Year': year,
            'Missing Months': 'All months missing'
        })

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = cleaned_temperature_low[(cleaned_temperature_low['STATION'] == station) & (cleaned_temperature_low['Year'] == year)]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        if missing_months:
            missing_years_list.append({
                'STATION': station,
                'Year': year,
                'Missing Months': sorted(missing_months)
            })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_years_df = pd.DataFrame(missing_years_list)

# แสดงข้อมูลที่หายไป
if not missing_years_df.empty:
    print("มีสถานีที่มีข้อมูลปีและเดือนหายไป:")
    print(missing_years_df)
else:
    print("ทุกสถานีมีข้อมูลปีและเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_temperature_low['Datetime'] = pd.to_datetime(cleaned_temperature_low['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_temperature_low['Year'] = cleaned_temperature_low['Datetime'].dt.year
cleaned_temperature_low['Month'] = cleaned_temperature_low['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
missing_months_summary = []

for station in cleaned_temperature_low['STATION'].unique():
    station_data = cleaned_temperature_low[cleaned_temperature_low['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
    missing_percentage = (missing_months_count / total_months) * 100

    # เก็บข้อมูลผลลัพธ์
    missing_months_summary.append({
        'STATION': station,
        'Total Missing Months': missing_months_count,
        'Percentage Missing': missing_percentage
    })

# สร้าง DataFrame สำหรับข้อมูลที่หายไป
missing_months_df = pd.DataFrame(missing_months_summary)

# แสดงข้อมูลที่หายไป
if not missing_months_df.empty:
    print("ข้อมูลเปอร์เซ็นต์ของเดือนที่หายไปสำหรับแต่ละสถานี:")
    print(missing_months_df)
else:
    print("ทุกสถานีมีข้อมูลเดือนครบถ้วน")

import pandas as pd

# เปลี่ยนคอลัมน์ 'Datetime' เป็นประเภทวันที่
cleaned_temperature_low['Datetime'] = pd.to_datetime(cleaned_temperature_low['Datetime'], format='%b-%y')

# สร้างคอลัมน์ใหม่สำหรับปีและเดือน
cleaned_temperature_low['Year'] = cleaned_temperature_low['Datetime'].dt.year
cleaned_temperature_low['Month'] = cleaned_temperature_low['Datetime'].dt.month

# ช่วงปีที่เราต้องการตรวจสอบ
start_year = 1998
end_year = 2023

# สร้าง DataFrame สำหรับการเก็บข้อมูลที่หายไป
total_months_all_stations = 0
missing_months_all_stations = 0

for station in cleaned_temperature_low['STATION'].unique():
    station_data = cleaned_temperature_low[cleaned_temperature_low['STATION'] == station]

    # สร้างชุดปีทั้งหมดที่คาดหวัง
    expected_years = set(range(start_year, end_year + 1))
    years_with_data = set(station_data['Year'])
    missing_years_in_station = expected_years - years_with_data

    total_months = len(expected_years) * 12  # จำนวนเดือนทั้งหมดที่คาดหวัง
    missing_months_count = 0

    # ตรวจสอบปีที่หายไป
    for year in missing_years_in_station:
        missing_months_count += 12  # ปีที่หายไปทั้งหมด 12 เดือน

    # ตรวจสอบเดือนที่หายไปในปีที่มีข้อมูล
    for year in years_with_data:
        year_data = station_data[station_data['Year'] == year]
        months_in_year = year_data['Month'].unique()
        all_months = set(range(1, 13))  # เดือน 1 ถึง 12
        missing_months = all_months - set(months_in_year)

        missing_months_count += len(missing_months)

    # อัปเดตค่าทั้งหมดสำหรับทุกสถานี
    total_months_all_stations += total_months
    missing_months_all_stations += missing_months_count

# คำนวณเปอร์เซ็นต์ของเดือนที่หายไป
missing_percentage_all_stations = (missing_months_all_stations / total_months_all_stations) * 100

# แสดงผลลัพธ์
print(f"รวมข้อมูลสำหรับทุกสถานีในช่วงปี {start_year}-{end_year}:")
print(f"จำนวนเดือนทั้งหมดที่คาดหวัง: {total_months_all_stations}")
print(f"จำนวนเดือนที่หายไป: {missing_months_all_stations}")
print(f"เปอร์เซ็นต์ของเดือนที่หายไป: {missing_percentage_all_stations:.2f}%")

# เปลี่ยนคอลัมน์ 'Datetime' ใน cleaned_rainfall_data เป็นประเภทวันที่
cleaned_temperature_low['Datetime'] = pd.to_datetime(cleaned_temperature_low['Datetime'], format='%b-%y')

# แสดง 10 แถวแรกของ DataFrame
cleaned_temperature_low.head(10)

# สร้างคอลัมน์ 'YEAR' จากคอลัมน์ 'Datetime'
cleaned_temperature_low['YEAR'] = cleaned_temperature_low['Datetime'].dt.year

# แสดง 10 แถวแรกของ DataFrame
cleaned_temperature_low.head(10)

# เปลี่ยนชื่อคอลัมน์เป็นตัวพิมพ์ใหญ่
cleaned_temperature_low.columns = [col.upper() for col in cleaned_temperature_low.columns]

# กำหนดชื่อคอลัมน์ใหม่ (ตัวพิมพ์ใหญ่)
new_columns = [
    'STATION', 'DATETIME',
    'DAY1', 'DAY2', 'DAY3', 'DAY4', 'DAY5', 'DAY6', 'DAY7', 'DAY8', 'DAY9',
    'DAY10', 'DAY11', 'DAY12', 'DAY13', 'DAY14', 'DAY15', 'DAY16', 'DAY17',
    'DAY18', 'DAY19', 'DAY20', 'DAY21', 'DAY22', 'DAY23', 'DAY24', 'DAY25',
    'DAY26', 'DAY27', 'DAY28', 'DAY29', 'DAY30', 'DAY31', 'AVERAGE'
]

# เลือกเฉพาะคอลัมน์ที่ต้องการใน DataFrame
cleaned_temperature_low = cleaned_temperature_low[new_columns]

# สร้างคอลัมน์ 'NO' และเพิ่ม "NO" ในทุกแถว
cleaned_temperature_low['NO'] = 'NO'

# จัดเรียงคอลัมน์ใหม่ให้อยู่ในลำดับที่ต้องการ
cleaned_temperature_low = cleaned_temperature_low[['NO'] + new_columns]

# แสดง 10 แถวแรกของ DataFrame
cleaned_temperature_low.head(10)
cleaned_temperature_low.shape
cleaned_temperature_low['NO'] = range(1, len(cleaned_temperature_low) + 1)
cleaned_temperature_low.head(10)
cleaned_temperature_low.drop(columns=['NO'])
cleaned_temperature_low.shape
## TEM
import pandas as pd

# โหลดข้อมูลทั้งสอง DataFrame (แทนที่ด้วยข้อมูลของคุณ)
temperature_high = cleaned_temperature_data # ข้อมูลอุณหภูมิสูง
temperature_low = cleaned_temperature_low # ข้อมูลอุณหภูมิต่ำ

# รีเซ็ตดัชนีทั้งสอง DataFrame
temperature_high_reset = temperature_high.reset_index(drop=True)
temperature_low_reset = temperature_low.reset_index(drop=True)

# ตรวจสอบข้อมูลที่มีใน temperature_high แต่ไม่มีใน temperature_low
merged_data = pd.merge(
    temperature_high_reset[['STATION', 'DATETIME']],
    temperature_low_reset[['STATION', 'DATETIME']],
    on=['STATION', 'DATETIME'],
    how='outer',
    indicator=True
)

# แสดงข้อมูลที่อยู่ใน temperature_high แต่ไม่อยู่ใน temperature_low
missing_in_temperature_low = merged_data[merged_data['_merge'] == 'left_only']
print("ข้อมูลที่มีใน temperature_high แต่ไม่มีใน temperature_low:")
print(missing_in_temperature_low)

# แสดงข้อมูลที่อยู่ใน temperature_low แต่ไม่อยู่ใน temperature_high
missing_in_temperature_high = merged_data[merged_data['_merge'] == 'right_only']
print("ข้อมูลที่มีใน temperature_low แต่ไม่มีใน temperature_high:")
print(missing_in_temperature_high)

# ถ้าต้องการตรวจสอบเฉพาะข้อมูลที่ตรงกันในทั้งสอง DataFrame เพื่อเปรียบเทียบ AVERAGE
common_data = pd.merge(
    temperature_high_reset,
    temperature_low_reset,
    on=['STATION', 'DATETIME'],
    suffixes=('_temperature_high', '_temperature_low')
)
temperature_high_reset.drop(columns=['NO'])
temperature_low_reset.drop(columns=['NO'])
import pandas as pd

# ตรวจสอบความยาวของ DataFrame
print(f"Length of temperature_high: {len(temperature_high)}")
print(f"Length of temperature_low: {len(temperature_low)}")

# ตรวจสอบคอลัมน์ 'AVERAGE'
assert 'AVERAGE' in temperature_high.columns, "Column 'AVERAGE' not found in temperature_high data."
assert 'AVERAGE' in temperature_low.columns, "Column 'AVERAGE' not found in temperature_low data."

# ทำการรวมข้อมูลที่ไม่ตรงกัน
common_dates = temperature_high['DATETIME'].isin(temperature_low['DATETIME'])
temperature_high = temperature_high[common_dates]
temperature_low = temperature_low[temperature_low['DATETIME'].isin(temperature_high['DATETIME'])]

# ตรวจสอบอีกครั้งว่าจำนวนแถวตรงกันแล้ว
print(f"Updated length of temperature_high: {len(temperature_high)}")
print(f"Updated length of temperature_low: {len(temperature_low)}")

# คำนวณค่าอุณหภูมิรายเดือน
def calculate_monthly_avg(high_df, low_df):
    # คำนวณค่าอุณหภูมิเฉลี่ยรายเดือนจากข้อมูลสูงสุดและต่ำสุด
    # Convert 'AVERAGE' columns to numeric type
    high_avg = pd.to_numeric(high_df['AVERAGE'], errors='coerce') # Convert to numeric, replace invalid values with NaN
    low_avg = pd.to_numeric(low_df['AVERAGE'], errors='coerce') # Convert to numeric, replace invalid values with NaN

    # คำนวณอุณหภูมิรายเดือน
    monthly_avg = (high_avg + low_avg) / 2

    # สร้าง DataFrame ใหม่สำหรับเก็บข้อมูลอุณหภูมิรายเดือน
    Tem = high_df[['STATION', 'DATETIME']].copy()
    Tem['MONTHLY_AVERAGE'] = monthly_avg

    return Tem

# คำนวณค่าอุณหภูมิเฉลี่ยรายเดือน
Tem = calculate_monthly_avg(temperature_high, temperature_low)

Tem