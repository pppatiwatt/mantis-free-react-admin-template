## Xgboost SPI

import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# แปลงคอลัมน์ 'DATETIME' เป็น datetime object
all_spi['DATETIME'] = pd.to_datetime(all_spi['DATETIME'])

# แยกข้อมูลสำหรับการฝึกและทดสอบ
train_data = all_spi[all_spi['DATETIME'].dt.year <= 2022]
test_data = all_spi[all_spi['DATETIME'].dt.year == 2023]

# จัดการข้อมูลที่หายไป
train_data = train_data.fillna(method='ffill')
test_data = test_data.fillna(method='ffill')

# รับรายการสถานี
stations = all_spi['STATION'].unique()

# ฟังก์ชันสำหรับการทำความสะอาดข้อมูล
def clean_data(df):
    mask = (df['SPI'].notna()) & (df['SPI'] != float('inf')) & (df['SPI'] != -float('inf'))
    return df[mask]

# สร้าง DataFrame เก็บผลลัพธ์การทำนายรายเดือน
predicted_spi_results_Xgboost = pd.DataFrame(columns=['DATETIME', 'STATION', 'Actual_SPI', 'Predicted_SPI'])

# สร้าง DataFrame เก็บผลลัพธ์การทำนายแบบไตรมาส
predicted_Quarterly_spi_results_Xgboost = pd.DataFrame(columns=['Quarter', 'STATION', 'Actual_SPI', 'Predicted_SPI'])

for station in stations:
    # กรองข้อมูลตามสถานี
    train_station = train_data[train_data['STATION'] == station]
    test_station = test_data[test_data['STATION'] == station]

    # ทำความสะอาดข้อมูล
    train_station = clean_data(train_station)
    test_station = clean_data(test_station)

    # ตรวจสอบว่ามีข้อมูลสำหรับปี 2023 หรือไม่
    if test_station.empty:
        print(f"No data available for 2023 at station {station}. Skipping this station.")
        continue

    # สร้าง features และ target
    X_train_station = train_station[['SPI']]  # ใช้เพียงค่า SPI เป็น feature
    y_train_station = train_station['SPI']     # ใช้ค่า SPI เป็น target
    X_test_station = test_station[['SPI']]     # ใช้เพียงค่า SPI เป็น feature
    y_test_station = test_station['SPI']       # ใช้ค่า SPI เป็น target

    # สร้าง DMatrix สำหรับ XGBoost
    dtrain_station = xgb.DMatrix(X_train_station, label=y_train_station)
    dtest_station = xgb.DMatrix(X_test_station, label=y_test_station)

    # กำหนดพารามิเตอร์ของโมเดล
    params = {
        'objective': 'reg:squarederror',
        'max_depth': 4,
        'learning_rate': 0.05,
        'n_estimators': 200,
        'subsample': 0.8,
        'colsample_bytree': 0.8
    }

    # ฝึกโมเดล
    model = xgb.train(params, dtrain_station, num_boost_round=200)

    # ทำนายผลสำหรับปี 2023
    Gxboost_spi_2023 = model.predict(dtest_station)

    # ประเมินผล
    mse = mean_squared_error(y_test_station, Gxboost_spi_2023)
    print(f"Station: {station}, Mean Squared Error for SPI prediction in 2023: {mse}")

    # แสดงผลการพยากรณ์เทียบกับค่าจริงปี 2023
    plt.figure(figsize=(12, 6))
    plt.plot(test_station['DATETIME'], y_test_station, label='Actual SPI 2023', marker='o')
    plt.plot(test_station['DATETIME'], Gxboost_spi_2023, label='Predicted SPI 2023', marker='x')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('SPI')
    plt.title(f'Station: {station} - Actual vs Predicted SPI for 2023')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # แสดงค่าพยากรณ์และค่าจริงสำหรับปี 2023
    print(f"\nPredicted vs Actual SPI for 2023 at station {station}:")
    for date, prediction, actual in zip(test_station['DATETIME'], Gxboost_spi_2023, y_test_station):
        print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}, Actual: {actual:.4f}")

    # เพิ่มผลลัพธ์การทำนายลงใน DataFrame สำหรับบันทึกผลรายเดือน
    station_results = pd.DataFrame({
        'DATETIME': test_station['DATETIME'].values,
        'STATION': station,
        'Actual_SPI': y_test_station,
        'Predicted_SPI': Gxboost_spi_2023
    })
    predicted_spi_results_Xgboost = pd.concat([predicted_spi_results_Xgboost, station_results], ignore_index=True)

    # คำนวณค่าเฉลี่ย SPI รายไตรมาส
    test_station['Quarter'] = test_station['DATETIME'].dt.to_period('Q')
    test_station['Gxboost_Predicted_SPI'] = Gxboost_spi_2023
    Gxboost_Quarterly_spi_2023 = test_station.groupby('Quarter').agg({
        'SPI': 'mean',  # Actual SPI
        'Gxboost_Predicted_SPI': 'mean'  # Predicted SPI
    }).rename(columns={'SPI': 'Actual_SPI', 'Gxboost_Predicted_SPI': 'Predicted_SPI'})

    # แสดงกราฟค่าเฉลี่ย SPI รายไตรมาส
    plt.figure(figsize=(10, 5))
    Gxboost_Quarterly_spi_2023[['Actual_SPI', 'Predicted_SPI']].plot(kind='bar', position=1, width=0.4, label=['Actual SPI', 'Predicted SPI'])
    plt.legend()
    plt.xlabel('Quarter')
    plt.ylabel('Average SPI')
    plt.title(f'Station: {station} - Quarterly Average SPI for 2023')
    plt.tight_layout()
    plt.show()

    # แสดงค่าเฉลี่ย SPI รายไตรมาส
    print(f"\nQuarterly Average SPI for 2023 at station {station}:")
    for quarter, row in Gxboost_Quarterly_spi_2023.iterrows():
        print(f"{quarter}: Actual SPI: {row['Actual_SPI']:.4f}, Predicted SPI: {row['Predicted_SPI']:.4f}")

    # เพิ่มผลลัพธ์รายไตรมาสลงใน DataFrame
    quarterly_results = pd.DataFrame({
        'Quarter': Gxboost_Quarterly_spi_2023.index.astype(str),
        'STATION': station,
        'Actual_SPI': Gxboost_Quarterly_spi_2023['Actual_SPI'],
        'Predicted_SPI': Gxboost_Quarterly_spi_2023['Predicted_SPI']
    })
    predicted_Quarterly_spi_results_Xgboost = pd.concat([predicted_Quarterly_spi_results_Xgboost, quarterly_results], ignore_index=True)

# บันทึกผลลัพธ์รายเดือนลง CSV
predicted_spi_results_Xgboost.to_csv('predicted_spi_results_Xgboost.csv', index=False, encoding='utf-8')
print("Monthly prediction results have been saved to 'predicted_spi_results_Xgboost.csv'")

# บันทึกผลลัพธ์รายไตรมาสลง CSV
predicted_Quarterly_spi_results_Xgboost.to_csv('predicted_Quarterly_spi_xgboost.csv', index=False, encoding='utf-8')
print("Quarterly prediction results have been saved to 'predicted_Quarterly_spi_xgboost.csv'")


import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# สมมติว่าคุณได้โหลดข้อมูล SPI เข้ามาแล้วในตัวแปร all_spi
# all_spi = pd.read_csv('path_to_spi_data.csv')

# แปลงคอลัมน์ 'DATETIME' เป็น datetime object
all_spi['DATETIME'] = pd.to_datetime(all_spi['DATETIME'])

# ใช้ข้อมูลทั้งหมดเป็นชุด training
train_data = all_spi

# จัดการข้อมูลที่หายไป
train_data = train_data.fillna(method='ffill')

# รับรายการสถานี
stations = all_spi['STATION'].unique()

# ฟังก์ชันสำหรับการทำความสะอาดข้อมูล
def clean_data(df):
    mask = (df['SPI'].notna()) & (df['SPI'] != float('inf')) & (df['SPI'] != -float('inf'))
    return df[mask]

# ฟังก์ชันสำหรับสร้างข้อมูลจำลองสำหรับปี 2024
def generate_2024_data(last_date):
    next_year = last_date.year + 1
    dates = pd.date_range(start=f'{next_year}-01-01', end=f'{next_year}-12-31', freq='MS')
    dummy_data = pd.DataFrame({'DATETIME': dates})
    dummy_data['SPI'] = dummy_data['DATETIME'].dt.month.map(train_data.groupby(train_data['DATETIME'].dt.month)['SPI'].mean())
    return dummy_data

for station in stations:
    # กรองข้อมูลตามสถานี
    train_station = train_data[train_data['STATION'] == station]

    # ทำความสะอาดข้อมูล
    train_station = clean_data(train_station)

    # สร้าง features และ target
    X_train_station = train_station[['SPI']]
    y_train_station = train_station['SPI']

    # สร้าง DMatrix สำหรับ XGBoost
    dtrain_station = xgb.DMatrix(X_train_station, label=y_train_station)

    # กำหนดพารามิเตอร์ของโมเดล
    params = {
        'objective': 'reg:squarederror',
        'max_depth': 4,
        'learning_rate': 0.05,
        'n_estimators': 200,
        'subsample': 0.8,
        'colsample_bytree': 0.8
    }

    # ฝึกโมเดล
    model = xgb.train(params, dtrain_station, num_boost_round=200)

    # สร้างข้อมูลจำลองสำหรับปี 2024
    last_date = train_station['DATETIME'].max()
    dummy_2024 = generate_2024_data(last_date)
    dummy_2024['STATION'] = station

    # ทำนายผลสำหรับปี 2024
    X_pred_2024 = dummy_2024[['SPI']]
    dpred_2024 = xgb.DMatrix(X_pred_2024)
    Gxboost_spi_2024 = model.predict(dpred_2024)

    # แสดงผลการพยากรณ์สำหรับปี 2024
    plt.figure(figsize=(12, 6))
    plt.plot(dummy_2024['DATETIME'], Gxboost_spi_2024, label='Predicted SPI 2024', marker='x')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('SPI')
    plt.title(f'Station: {station} - Predicted SPI for 2024')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # แสดงค่าพยากรณ์สำหรับปี 2024
    print(f"\nPredicted SPI for 2024 at station {station}:")
    for date, prediction in zip(dummy_2024['DATETIME'], Gxboost_spi_2024):
        print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}")

    # คำนวณค่าเฉลี่ย SPI รายไตรมาสสำหรับปี 2024
    dummy_2024['Quarter'] = dummy_2024['DATETIME'].dt.to_period('Q')
    dummy_2024['Gxboost_Predicted_SPI'] = Gxboost_spi_2024
    Gxboost_Quarterly_spi_2024 = dummy_2024.groupby('Quarter')['Gxboost_Predicted_SPI'].mean()

    # แสดงกราฟค่าเฉลี่ย SPI รายไตรมาสสำหรับปี 2024
    plt.figure(figsize=(10, 5))
    Gxboost_Quarterly_spi_2024.plot(kind='bar')
    plt.legend(['Predicted SPI'])
    plt.xlabel('Quarter')
    plt.ylabel('Average SPI')
    plt.title(f'Station: {station} - Quarterly Average Predicted SPI for 2024')
    plt.tight_layout()
    plt.show()

    # แสดงค่าเฉลี่ย SPI รายไตรมาสสำหรับปี 2024
    print(f"\nQuarterly Average Predicted SPI for 2024 at station {station}:")
    for quarter, value in Gxboost_Quarterly_spi_2024.items():
        print(f"{quarter}: Predicted: {value:.4f}")
