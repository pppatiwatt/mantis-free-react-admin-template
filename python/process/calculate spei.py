# นี่คือขั้นตอนการคำนวณหาค่า spei
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