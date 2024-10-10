# นี่คือขั้นตอนการฝึกโมเดล random forest spi

##Random Forest SPI

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
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

# สร้าง DataFrame สำหรับเก็บผลลัพธ์การทำนาย
predicted_spi_results_RandomForest = pd.DataFrame(columns=['DATETIME', 'STATION', 'Actual_SPI', 'Predicted_SPI'])

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
    X_train_station = train_station[['SPI']]
    y_train_station = train_station['SPI']
    X_test_station = test_station[['SPI']]
    y_test_station = test_station['SPI']

    # สร้างและฝึกโมเดล Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_station, y_train_station)

    # ทำนายผลสำหรับปี 2023
    RandomForest_spi_2023 = model.predict(X_test_station)

    # ประเมินผล
    mse = mean_squared_error(y_test_station, RandomForest_spi_2023)
    print(f"Station: {station}, Mean Squared Error for SPI prediction in 2023: {mse}")

    # แสดงผลการพยากรณ์เทียบกับค่าจริงปี 2023
    plt.figure(figsize=(12, 6))
    plt.plot(test_station['DATETIME'], y_test_station, label='Actual SPI 2023', marker='o')
    plt.plot(test_station['DATETIME'], RandomForest_spi_2023, label='Predicted SPI 2023', marker='x')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('SPI')
    plt.title(f'Station: {station} - Actual vs Predicted SPI for 2023')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # แสดงค่าพยากรณ์และค่าจริงสำหรับปี 2023
    print(f"\nPredicted vs Actual SPI for 2023 at station {station}:")
    for date, prediction, actual in zip(test_station['DATETIME'], RandomForest_spi_2023, y_test_station):
        print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}, Actual: {actual:.4f}")

    # เพิ่มผลลัพธ์การทำนายลงใน DataFrame สำหรับบันทึกผล
    station_results = pd.DataFrame({
        'DATETIME': test_station['DATETIME'],
        'STATION': station,
        'Actual_SPI': y_test_station,
        'Predicted_SPI': RandomForest_spi_2023
    })
    predicted_spi_results_RandomForest = pd.concat([predicted_spi_results_RandomForest, station_results], ignore_index=True)

    # คำนวณค่าเฉลี่ย SPI รายไตรมาส
    test_station['Quarter'] = test_station['DATETIME'].dt.to_period('Q')
    test_station['RandomForest_Predicted_SPI'] = RandomForest_spi_2023
    quarterly_data = test_station.groupby('Quarter').agg({
        'SPI': 'mean',  # Actual SPI
        'RandomForest_Predicted_SPI': 'mean'  # Predicted SPI
    }).rename(columns={'SPI': 'Actual_SPI', 'RandomForest_Predicted_SPI': 'Predicted_SPI'})

    # แสดงค่าเฉลี่ย SPI รายไตรมาส
    print(f"\nQuarterly Average SPI for 2023 at station {station}:")
    for quarter, row in quarterly_data.iterrows():
        print(f"{quarter}: Actual SPI: {row['Actual_SPI']:.4f}, Predicted SPI: {row['Predicted_SPI']:.4f}")

# บันทึกผลลัพธ์รายเดือนลงใน CSV
predicted_spi_results_RandomForest.to_csv('predicted_spi_results_RandomForest.csv', index=False, encoding='utf-8')
print("Monthly prediction results have been saved to 'predicted_spi_results_RandomForest.csv'")