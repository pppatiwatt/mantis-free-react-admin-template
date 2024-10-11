# SPI
import pandas as pd
import numpy as np
from scipy.stats import norm

# ตรวจสอบและจัดการค่าที่เป็น 'T' หรือ '-'
cleaned_rainfall_data['RAINFALL'] = cleaned_rainfall_data['RAINFALL'].replace(['T', '-'], np.nan).astype(float)

# คำนวณค่าเฉลี่ยและค่าเบี่ยงเบนมาตรฐานของปริมาณน้ำฝนที่ไม่เป็น NaN
mean_rainfall = cleaned_rainfall_data['RAINFALL'].mean()
std_rainfall = cleaned_rainfall_data['RAINFALL'].std()

# สร้างฟังก์ชันสำหรับคำนวณ SPI
def calculate_spi(rainfall, mean, std):
    if np.isnan(rainfall):  # ถ้าค่า Rainfall เป็น NaN (เช่น 'T' หรือ '-')
        return np.nan  # ใช้ NaN แทน '-'
    if std == 0:  # ถ้า std เป็น 0 ให้คืนค่า NaN
        return np.nan
    else:
        # คำนวณค่า Z-score สำหรับ SPI
        return (rainfall - mean) / std

# คำนวณค่า SPI และเพิ่มเป็นคอลัมน์ใหม่ใน DataFrame
cleaned_rainfall_data['SPI'] = cleaned_rainfall_data['RAINFALL'].apply(calculate_spi, args=(mean_rainfall, std_rainfall))

# เก็บค่า SPI ออกมาในตัวแปร all_spi
all_spi = cleaned_rainfall_data[['STATION', 'DATETIME', 'SPI']].copy()

all_spi

all_spi.shape
all_spi.dropna()
all_spi.shape

# SPEI
import pandas as pd
import numpy as np

# อ่านข้อมูล
rainfall_data = cleaned_rainfall_data
evaporation_data = cleaned_evaporation_data
temperature_data = Tem

# ฟังก์ชันคำนวณค่า PET โดยใช้ Thornthwaite (ต้องการอุณหภูมิรายเดือน)
def thornthwaite_pet(temp_mean):
    # คำนวณค่า I (thermal index)
    I = np.sum((temp_mean / 5) ** 1.514)

    # คำนวณค่า a โดยใช้สูตร Thornthwaite
    a = 6.75e-7 * I**3 - 7.71e-5 * I**2 + 1.792e-2 * I + 0.49239

    # คำนวณค่า PET โดยใช้สูตร Thornthwaite
    pet = 16 * ((10 * temp_mean / I) ** a)
    return pet

# ตรวจสอบและจัดการค่า NaN ในข้อมูล
def preprocess_data(df):
    df = df.replace(['T', '-'], np.nan).astype(float)
    return df

# ประมวลผลข้อมูล
rainfall_data['RAINFALL'] = preprocess_data(rainfall_data['RAINFALL'])
evaporation_data['EVAPORATION'] = preprocess_data(evaporation_data['EVAPORATION'])
temperature_data['MONTHLY_AVERAGE'] = preprocess_data(temperature_data['MONTHLY_AVERAGE'])

# หาสถานีที่ไม่ซ้ำกัน
stations = rainfall_data['STATION'].unique()

# สร้าง DataFrame ว่างเพื่อเก็บผลลัพธ์
all_spei_results = pd.DataFrame()

# วนลูปผ่านแต่ละสถานี
for station in stations:
    # กรองข้อมูลสำหรับสถานีปัจจุบัน
    station_rainfall = rainfall_data[rainfall_data['STATION'] == station]
    station_temperature = temperature_data[temperature_data['STATION'] == station]

    # ตรวจสอบว่ามีข้อมูลทั้งสองประเภท
    if station_rainfall.empty or station_temperature.empty:
        print(f"Warning: No data for station {station}")
        continue

    # คำนวณค่า PET โดยใช้ข้อมูลอุณหภูมิรายเดือน
    station_temperature['PET'] = station_temperature['MONTHLY_AVERAGE'].apply(thornthwaite_pet)

    # รวมข้อมูลการฝนตกและ PET
    combined_data = station_rainfall.merge(station_temperature[['DATETIME', 'PET']], on='DATETIME', how='inner')

    # คำนวณดัชนีความชื้น
    combined_data['W'] = combined_data['RAINFALL'] - combined_data['PET']

    # คำนวณค่าเฉลี่ยและค่าเบี่ยงเบนมาตรฐานของดัชนีความชื้น
    mean_w = combined_data['W'].mean()
    std_w = combined_data['W'].std()

    # คำนวณค่า SPEI
    combined_data['SPEI'] = (combined_data['W'] - mean_w) / std_w

    # เลือกเฉพาะคอลัมน์ที่ต้องการ
    selected_columns = combined_data[['STATION', 'DATETIME', 'PET', 'W', 'SPEI']]

    # เพิ่มผลลัพธ์ลงใน DataFrame all_spei_results
    all_spei_results = pd.concat([all_spei_results, selected_columns], ignore_index=True)

# แสดงผลลัพธ์สุดท้าย
all_spei_results

all_spei_results.shape
all_spei_results.dropna()
all_spei_results.shape