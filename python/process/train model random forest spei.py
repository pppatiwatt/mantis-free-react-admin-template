# นี่คือขั้นตอนการฝึกโมเดล random forest spei

## Random Forest SPEI

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

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

# สร้าง DataFrame เก็บผลลัพธ์การทำนาย
predicted_spei_results_RandomForest = pd.DataFrame(columns=['DATETIME', 'STATION', 'Actual_SPEI', 'Predicted_SPEI'])

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

    # สร้างและฝึกโมเดล Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_station, y_train_station)

    # ทำนายผลสำหรับปี 2023
    RandomForest_spei_2023 = model.predict(X_test_station)

    # ประเมินผล
    mse = mean_squared_error(y_test_station, RandomForest_spei_2023)
    print(f"Station: {station}, Mean Squared Error for 2023: {mse}")

    # เพิ่มผลลัพธ์การทำนายลงใน DataFrame
    station_results = pd.DataFrame({
        'DATETIME': test_station['DATETIME'],
        'STATION': station,
        'Actual_SPEI': y_test_station,
        'Predicted_SPEI': RandomForest_spei_2023
    })
    predicted_spei_results_RandomForest = pd.concat([predicted_spei_results_RandomForest, station_results], ignore_index=True)

    # แสดงผลการพยากรณ์เทียบกับค่าจริงปี 2023
    plt.figure(figsize=(12, 6))
    plt.plot(test_station['DATETIME'], y_test_station, label='Actual SPEI 2023', marker='o')
    plt.plot(test_station['DATETIME'], RandomForest_spei_2023, label='Predicted SPEI 2023', marker='x')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('SPEI')
    plt.title(f'Station: {station} - Actual vs Predicted SPEI for 2023 (Random Forest)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # แสดงค่าพยากรณ์และค่าจริงสำหรับปี 2023
    print(f"\nPredicted vs Actual SPEI for 2023 at station {station}:")
    for date, prediction, actual in zip(test_station['DATETIME'], RandomForest_spei_2023, y_test_station):
        print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}, Actual: {actual:.4f}")

    # คำนวณค่าเฉลี่ย SPEI รายไตรมาส
    test_station['Quarter'] = test_station['DATETIME'].dt.to_period('Q')
    test_station['RandomForest_Predicted_SPEI'] = RandomForest_spei_2023
    RandomForest_Quarterly_spei_2023 = test_station.groupby('Quarter').agg({
        'SPEI': 'mean',
        'RandomForest_Predicted_SPEI': 'mean'
    }).rename(columns={'SPEI': 'Actual', 'RandomForest_Predicted_SPEI': 'Predicted'})

    # แสดงกราฟค่าเฉลี่ย SPEI รายไตรมาส
    plt.figure(figsize=(10, 5))
    RandomForest_Quarterly_spei_2023[['Actual', 'Predicted']].plot(kind='bar', position=1, width=0.4, label=['Actual SPEI', 'Predicted SPEI'])
    plt.legend()
    plt.xlabel('Quarter')
    plt.ylabel('Average SPEI')
    plt.title(f'Station: {station} - Quarterly Average SPEI for 2023 (Random Forest)')
    plt.tight_layout()
    plt.show()

    # แสดงค่าเฉลี่ย SPEI รายไตรมาส
    print(f"\nQuarterly Average SPEI for 2023 at station {station}:")
    for quarter, row in RandomForest_Quarterly_spei_2023.iterrows():
        print(f"{quarter}: Actual: {row['Actual']:.4f}, Predicted: {row['Predicted']:.4f}")

    # แสดงความสำคัญของ features
    feature_importance = model.feature_importances_
    features = ['PET', 'W']
    plt.figure(figsize=(8, 4))
    plt.bar(features, feature_importance)
    plt.title(f'Feature Importance for SPEI Prediction at station {station}')
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.tight_layout()
    plt.show()

    print(f"\nFeature Importance for SPEI Prediction at station {station}:")
    for feature, importance in zip(features, feature_importance):
        print(f"{feature}: {importance:.4f}")

# บันทึกผลลัพธ์ลง CSV พร้อมระบุ encoding เป็น UTF-8
predicted_spei_results_RandomForest.to_csv('predicted_spei_results_RandomForest.csv', index=False, encoding='utf-8')
print("Results have been saved to 'predicted_spei_results_RandomForest.csv'")