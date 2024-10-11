## Xgboost SPEI

import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import csv

# แปลงคอลัมน์ 'DATETIME' เป็น datetime object
all_spei_results['DATETIME'] = pd.to_datetime(all_spei_results['DATETIME'])

# แยกชุดฝึกและชุดทดสอบตามปี
train_data = all_spei_results[all_spei_results['DATETIME'].dt.year <= 2022]
test_data = all_spei_results[all_spei_results['DATETIME'].dt.year == 2023]

# จัดการข้อมูลที่หายไป
train_data = train_data.fillna(method='ffill')
test_data = test_data.fillna(method='ffill')

# รับรายการสถานี
stations = all_spei_results['STATION'].unique()

# ฟังก์ชันสำหรับการทำความสะอาดข้อมูล
def clean_data(df):
    mask = (df['SPEI'].notna()) & (df['SPEI'] != float('inf')) & (df['SPEI'] != -float('inf'))
    return df[mask]

# เปิดไฟล์ CSV เพื่อบันทึกผลลัพธ์รายเดือน
with open('predicted_spei_results_Xgboost.csv', mode='w', newline='', encoding='utf-8') as file_monthly, \
     open('predicted_Quarterly_spei_xgboost.csv', mode='w', newline='', encoding='utf-8') as file_quarterly:

    writer_monthly = csv.writer(file_monthly)
    writer_quarterly = csv.writer(file_quarterly)

    # ปรับหัวคอลัมน์ตามที่ต้องการ
    writer_monthly.writerow(['STATION', 'DATETIME', 'Actual_SPEI', 'Predicted_SPEI'])
    writer_quarterly.writerow(['STATION', 'Quarter', 'Actual_SPEI', 'Predicted_SPEI'])

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
        X_train_station = train_station[['PET', 'W']]
        y_train_station = train_station['SPEI']
        X_test_station = test_station[['PET', 'W']]
        y_test_station = test_station['SPEI']

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
        Xgboost_spei_2023 = model.predict(dtest_station)

        # ประเมินผล
        mse = mean_squared_error(y_test_station, Xgboost_spei_2023)
        print(f"Station: {station}, Mean Squared Error for 2023: {mse}")

        # แสดงผลการพยากรณ์เทียบกับค่าจริงปี 2023
        plt.figure(figsize=(12, 6))
        plt.plot(test_station['DATETIME'], y_test_station, label='Actual SPEI 2023', marker='o')
        plt.plot(test_station['DATETIME'], Xgboost_spei_2023, label='Predicted SPEI 2023', marker='x')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('SPEI')
        plt.title(f'Station: {station} - Actual vs Predicted SPEI for 2023')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # แสดงค่าพยากรณ์และค่าจริงสำหรับปี 2023 และบันทึกผลลัพธ์รายเดือนลงในไฟล์ CSV
        print(f"\nPredicted vs Actual SPEI for 2023 at station {station}:")
        for date, prediction, actual in zip(test_station['DATETIME'], Xgboost_spei_2023, y_test_station):
            print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}, Actual: {actual:.4f}")
            # บันทึกเฉพาะผลลัพธ์รายเดือน
            writer_monthly.writerow([station, date.strftime('%Y-%m-%d'), actual, prediction])

        # คำนวณค่าเฉลี่ย SPEI รายไตรมาส
        test_station['Quarter'] = test_station['DATETIME'].dt.to_period('Q')
        test_station['Xgboost_Predicted_SPEI'] = Xgboost_spei_2023
        Xgboost_Quarterly_spei = test_station.groupby('Quarter').agg({
            'SPEI': 'mean',  # Actual SPEI
            'Xgboost_Predicted_SPEI': 'mean'  # Predicted SPEI
        }).rename(columns={'SPEI': 'Actual_SPEI', 'Xgboost_Predicted_SPEI': 'Predicted_SPEI'})

        # บันทึกผลลัพธ์รายไตรมาสลงในไฟล์ CSV
        for quarter, row in Xgboost_Quarterly_spei.iterrows():
            writer_quarterly.writerow([station, str(quarter), row['Actual_SPEI'], row['Predicted_SPEI']])

        # แสดงกราฟค่าเฉลี่ย SPEI รายไตรมาส (ไม่บันทึกลงไฟล์ CSV)
        plt.figure(figsize=(10, 5))
        Xgboost_Quarterly_spei[['Actual_SPEI', 'Predicted_SPEI']].plot(kind='bar', position=1, width=0.4, label=['Actual SPEI', 'Predicted SPEI'])
        plt.legend()
        plt.xlabel('Quarter')
        plt.ylabel('Average SPEI')
        plt.title(f'Station: {station} - Quarterly Average SPEI for 2023')
        plt.tight_layout()
        plt.show()

        # แสดงค่าเฉลี่ย SPEI รายไตรมาส
        print(f"\nQuarterly Average SPEI for 2023 at station {station}:")
        for quarter, row in Xgboost_Quarterly_spei.iterrows():
            print(f"{quarter}: Actual SPEI: {row['Actual_SPEI']:.4f}, Predicted SPEI: {row['Predicted_SPEI']:.4f}")


import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# แปลงคอลัมน์ 'DATETIME' เป็น datetime object
all_spei_results['DATETIME'] = pd.to_datetime(all_spei_results['DATETIME'])

# ใช้ข้อมูลทั้งหมดเป็นชุด training
train_data = all_spei_results

# จัดการข้อมูลที่หายไป
train_data = train_data.fillna(method='ffill')

# รับรายการสถานี
stations = all_spei_results['STATION'].unique()

# ฟังก์ชันสำหรับการทำความสะอาดข้อมูล
def clean_data(df):
    mask = (df['SPEI'].notna()) & (df['SPEI'] != float('inf')) & (df['SPEI'] != -float('inf'))
    return df[mask]

# ฟังก์ชันสำหรับสร้างข้อมูลจำลองสำหรับปี 2024
def generate_2024_data(last_date, features):
    next_year = last_date.year + 1
    dates = pd.date_range(start=f'{next_year}-01-01', end=f'{next_year}-12-31', freq='MS')
    dummy_data = pd.DataFrame({'DATETIME': dates})
    for feature in features:
        dummy_data[feature] = dummy_data['DATETIME'].dt.month.map(train_data.groupby(train_data['DATETIME'].dt.month)[feature].mean())
    return dummy_data

for station in stations:
    # กรองข้อมูลตามสถานี
    train_station = train_data[train_data['STATION'] == station]

    # ทำความสะอาดข้อมูล
    train_station = clean_data(train_station)

    # สร้าง features และ target
    X_train_station = train_station[['PET', 'W']]
    y_train_station = train_station['SPEI']

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
    dummy_2024 = generate_2024_data(last_date, ['PET', 'W'])
    dummy_2024['STATION'] = station

    # ทำนายผลสำหรับปี 2024
    X_pred_2024 = dummy_2024[['PET', 'W']]
    dpred_2024 = xgb.DMatrix(X_pred_2024)
    Gxboost_spei_2024 = model.predict(dpred_2024)

    # แสดงผลการพยากรณ์สำหรับปี 2024
    plt.figure(figsize=(12, 6))
    plt.plot(dummy_2024['DATETIME'], Gxboost_spei_2024, label='Predicted SPEI 2024', marker='x')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('SPEI')
    plt.title(f'Station: {station} - Predicted SPEI for 2024')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # แสดงค่าพยากรณ์สำหรับปี 2024
    print(f"\nPredicted SPEI for 2024 at station {station}:")
    for date, prediction in zip(dummy_2024['DATETIME'], Gxboost_spei_2024):
        print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}")

    # คำนวณค่าเฉลี่ย SPEI รายไตรมาสสำหรับปี 2024
    dummy_2024['Quarter'] = dummy_2024['DATETIME'].dt.to_period('Q')
    dummy_2024['Gxboost_Predicted_SPEI'] = Gxboost_spei_2024
    Gxboost_Quarterly_spei_2024 = dummy_2024.groupby('Quarter')['Gxboost_Predicted_SPEI'].mean()

    # แสดงกราฟค่าเฉลี่ย SPEI รายไตรมาสสำหรับปี 2024
    plt.figure(figsize=(10, 5))
    Gxboost_Quarterly_spei_2024.plot(kind='bar')
    plt.legend(['Predicted SPEI'])
    plt.xlabel('Quarter')
    plt.ylabel('Average SPEI')
    plt.title(f'Station: {station} - Quarterly Average Predicted SPEI for 2024')
    plt.tight_layout()
    plt.show()

    # แสดงค่าเฉลี่ย SPEI รายไตรมาสสำหรับปี 2024
    print(f"\nQuarterly Average Predicted SPEI for 2024 at station {station}:")
    for quarter, value in Gxboost_Quarterly_spei_2024.items():
        print(f"{quarter}: Predicted: {value:.4f}")
