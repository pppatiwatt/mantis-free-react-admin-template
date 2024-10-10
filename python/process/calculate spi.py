# นี่คือขั้นตอนการคำนวณหาค่า spi
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