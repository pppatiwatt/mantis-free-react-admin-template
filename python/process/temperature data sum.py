# นี่คือขั้นตอนรวมชุดข้อมูลอุณหภูมิ Temperature max ( อุณหภูมิสูงสุด ) Temperature min ( อุณหภูมิต่ำสุด ) เข้าด้วยกัน
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