import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import warnings
import matplotlib.font_manager as fm
import os
import requests

warnings.filterwarnings("ignore")

# ฟังก์ชันสำหรับดาวน์โหลดและตั้งค่าฟอนต์ภาษาไทย
def setup_thai_font():
    font_dir = 'fonts'
    os.makedirs(font_dir, exist_ok=True)
    font_url = 'https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf'
    font_path = os.path.join(font_dir, 'Sarabun-Regular.ttf')
    if not os.path.exists(font_path):
        response = requests.get(font_url)
        with open(font_path, 'wb') as f:
            f.write(response.content)
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'Sarabun'

# เรียกใช้ฟังก์ชันเพื่อตั้งค่าฟอนต์
setup_thai_font()

# ฟังก์ชันสำหรับโหลดและทำความสะอาดข้อมูล
def load_and_clean_data(file_paths, data_type):
    data = pd.DataFrame()
    for file_path in file_paths:
        temp_df = pd.read_csv(file_path, header=None)
        data = pd.concat([data, temp_df], ignore_index=True)
    
    print(f"Columns in {data_type} data:", data.columns)
    
    # กำหนดชื่อคอลัมน์ใหม่ตามลำดับ
    new_column_names = ['NO', 'STATION', 'DATETIME'] + [f'DAY{i}' for i in range(1, 32)] + ['TOTAL']
    data.columns = new_column_names

    if data_type == 'rainfall':
        data = data.rename(columns={'TOTAL': 'RAINFALL'})
    elif data_type == 'evaporation':
        data = data.rename(columns={'TOTAL': 'EVAPORATION'})
    elif data_type in ['temperature_max', 'temperature_min']:
        data = data.rename(columns={'TOTAL': 'AVERAGE'})

    # เลือกเฉพาะคอลัมน์ที่ต้องการ
    if data_type == 'rainfall':
        columns = ['NO', 'STATION', 'DATETIME', 'RAINFALL']
    elif data_type == 'evaporation':
        columns = ['STATION', 'DATETIME', 'EVAPORATION']
    elif data_type in ['temperature_max', 'temperature_min']:
        columns = ['STATION', 'DATETIME', 'AVERAGE']
    
    data = data[columns]
    
    data['DATETIME'] = pd.to_datetime(data['DATETIME'], format='%b-%y', errors='coerce')
    if data_type in ['rainfall', 'evaporation', 'temperature_max', 'temperature_min']:
        data[columns[-1]] = pd.to_numeric(data[columns[-1]].replace(['T', '-'], np.nan), errors='coerce')
    
    # ลบแถวที่มีค่า NaN
    data = data.dropna()
    
    return data

# ฟังก์ชันสำหรับคำนวณอุณหภูมิเฉลี่ย
def calculate_average_temperature(max_temp, min_temp):
    return pd.merge(max_temp, min_temp, on=['STATION', 'DATETIME'], suffixes=('_max', '_min'))

# ฟังก์ชันสำหรับคำนวณ SPI และ SPEI
def calculate_climate_index(data, index_type):
    if index_type == 'SPI':
        mean = data['RAINFALL'].mean()
        std = data['RAINFALL'].std()
        data['INDEX'] = (data['RAINFALL'] - mean) / std
    elif index_type == 'SPEI':
        # คำนวณ PET โดยใช้ Thornthwaite
        def thornthwaite_pet(temp_mean):
            I = np.sum((temp_mean / 5) ** 1.514)
            a = 6.75e-7 * I**3 - 7.71e-5 * I**2 + 1.792e-2 * I + 0.49239
            return 16 * ((10 * temp_mean / I) ** a)
        
        data['AVERAGE_TEMP'] = (data['AVERAGE_max'] + data['AVERAGE_min']) / 2
        data['PET'] = data['AVERAGE_TEMP'].apply(thornthwaite_pet)
        data['W'] = data['RAINFALL'] - data['PET']
        mean_w = data['W'].mean()
        std_w = data['W'].std()
        data['INDEX'] = (data['W'] - mean_w) / std_w
    
    # ลบแถวที่มีค่า NaN ในคอลัมน์ INDEX
    data = data.dropna(subset=['INDEX'])
    
    return data

# ฟังก์ชันสำหรับสร้างโมเดลและทำนาย
def create_and_predict_model(train_data, test_data, features, target):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_data[features], train_data[target])
    predictions = model.predict(test_data[features])
    mse = mean_squared_error(test_data[target], predictions)
    return predictions, mse, model

# ฟังก์ชันสำหรับแสดงผลและบันทึกผลลัพธ์ (ปรับปรุงให้แสดงภาษาไทย)
def plot_and_save_results(test_data, predictions, station, index_type):
    plt.figure(figsize=(12, 6))
    plt.plot(test_data['DATETIME'], test_data['INDEX'], label=f'ค่าจริง {index_type}', marker='o')
    plt.plot(test_data['DATETIME'], predictions, label=f'ค่าพยากรณ์ {index_type}', marker='x')
    plt.legend()
    plt.xlabel('เวลา')
    plt.ylabel(index_type)
    plt.title(f'สถานี: {station} - ค่าจริง vs ค่าพยากรณ์ {index_type} สำหรับปี 2023')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # คำนวณค่าเฉลี่ยรายไตรมาส
    test_data['Quarter'] = test_data['DATETIME'].dt.to_period('Q')
    test_data['Predicted'] = predictions
    quarterly_data = test_data.groupby('Quarter').agg({
        'INDEX': 'mean',
        'Predicted': 'mean'
    }).rename(columns={'INDEX': 'Actual', 'Predicted': 'Predicted'})

    # แสดงกราฟค่าเฉลี่ยรายไตรมาส
    plt.figure(figsize=(10, 5))
    quarterly_data[['Actual', 'Predicted']].plot(kind='bar', position=1, width=0.4)
    plt.legend(['ค่าจริง', 'ค่าพยากรณ์'])
    plt.xlabel('ไตรมาส')
    plt.ylabel(f'ค่าเฉลี่ย {index_type}')
    plt.title(f'สถานี: {station} - ค่าเฉลี่ยรายไตรมาส {index_type} สำหรับปี 2023')
    plt.tight_layout()
    plt.show()

    return quarterly_data

# โหลดและทำความสะอาดข้อมูล
rainfall_files = [
    r"python\Data\Rain\Rain-N1-2003-1998.csv",
    r"python\Data\Rain\Rain-N2-2003-1998.csv",
    r"python\Data\Rain\Rain-N1-2013-2004.csv",
    r"python\Data\Rain\Rain-N2-2013-2004.csv",
    r"python\Data\Rain\Rain-N1-2023-2014.csv",
    r"python\Data\Rain\Rain-N2-2023-2014.csv"
]
evaporation_files = [
    r"python\Data\eva\eva-d-N-1-1998-2003.csv",
    r"python\Data\eva\eva-d-N-2-1998-2003.csv",
    r"python\Data\eva\eva-d-N-1-2004-2013.csv",
    r"python\Data\eva\eva-d-N-2-2004-2013.csv",
    r"python\Data\eva\eva-d-N-1-2014-2023.csv",
    r"python\Data\eva\eva-d-N-2-2014-2023.csv"
]
temperature_max_files = [
    r"python\Data\MaxT\MaxT-N1-2003-1998.csv",
    r"python\Data\MaxT\MaxT-N2-2003-1998.csv",
    r"python\Data\MaxT\MaxT-N1-2013-2004.csv",
    r"python\Data\MaxT\MaxT-N2-2013-2004.csv",
    r"python\Data\MaxT\MaxT-N1-2023-2014.csv",
    r"python\Data\MaxT\MaxT-N2-2023-2014.csv"
]
temperature_min_files = [
    r"python\Data\MinT\MinT-N1-2003-1998.csv",
    r"python\Data\MinT\MinT-N2-2003-1998.csv",
    r"python\Data\MinT\MinT-N1-2013-2004.csv",
    r"python\Data\MinT\MinT-N2-2013-2004.csv",
    r"python\Data\MinT\MinT-N1-2023-2014.csv",
    r"python\Data\MinT\MinT-N2-2023-2014.csv"
]

rainfall_data = load_and_clean_data(rainfall_files, 'rainfall')
evaporation_data = load_and_clean_data(evaporation_files, 'evaporation')
temperature_max_data = load_and_clean_data(temperature_max_files, 'temperature_max')
temperature_min_data = load_and_clean_data(temperature_min_files, 'temperature_min')

# คำนวณอุณหภูมิเฉลี่ย
temperature_data = calculate_average_temperature(temperature_max_data, temperature_min_data)

# คำนวณ SPI และ SPEI
spi_data = calculate_climate_index(rainfall_data, 'SPI')
spei_data = calculate_climate_index(pd.merge(rainfall_data, temperature_data, on=['STATION', 'DATETIME']), 'SPEI')

# แบ่งข้อมูลฝึกและทดสอบ
train_data_spi = spi_data[spi_data['DATETIME'].dt.year <= 2022]
test_data_spi = spi_data[spi_data['DATETIME'].dt.year == 2023]
train_data_spei = spei_data[spei_data['DATETIME'].dt.year <= 2022]
test_data_spei = spei_data[spei_data['DATETIME'].dt.year == 2023]

# สร้าง DataFrame สำหรับเก็บผลลัพธ์
results = pd.DataFrame(columns=['DATETIME', 'STATION', 'INDEX_TYPE', 'ACTUAL', 'PREDICTED', 'QUARTER'])

# วนลูปผ่านแต่ละสถานีและทำนายทั้ง SPI และ SPEI
stations = spi_data['STATION'].unique()
for station in stations:
    for index_type, (train_data, test_data) in {'SPI': (train_data_spi, test_data_spi), 'SPEI': (train_data_spei, test_data_spei)}.items():
        station_train = train_data[train_data['STATION'] == station]
        station_test = test_data[test_data['STATION'] == station]
        
        # ตรวจสอบว่ามีข้อมูลเพียงพอสำหรับการสร้างโมเดลและทำนาย
        if len(station_train) < 10 or len(station_test) < 1:
            print(f"Insufficient data for station {station} for {index_type}. Skipping.")
            continue
        
        features = ['INDEX'] if index_type == 'SPI' else ['PET', 'W']
        
        # ตรวจสอบว่ามีค่า NaN หรือ inf หรือไม่
        if (station_train[features + ['INDEX']].isnull().values.any() or 
            station_test[features + ['INDEX']].isnull().values.any() or
            np.isinf(station_train[features + ['INDEX']]).values.any() or
            np.isinf(station_test[features + ['INDEX']]).values.any()):
            print(f"Warning: NaN or inf values found in {index_type} data for station {station}. Skipping this station.")
            continue
        
        try:
            predictions, mse, model = create_and_predict_model(station_train, station_test, features, 'INDEX')
            print(f"Station: {station}, {index_type} Mean Squared Error for 2023: {mse}")
            
            quarterly_data = plot_and_save_results(station_test, predictions, station, index_type)
            
            # เพิ่มผลลัพธ์ลงใน DataFrame
            for date, actual, predicted in zip(station_test['DATETIME'], station_test['INDEX'], predictions):
                quarter = date.to_period('Q')
                results = results.append({
                    'DATETIME': date,
                    'STATION': station,
                    'INDEX_TYPE': index_type,
                    'ACTUAL': actual,
                    'PREDICTED': predicted,
                    'QUARTER': quarter
                }, ignore_index=True)
            
            # แสดงความสำคัญของ features (เฉพาะ SPEI)
            if index_type == 'SPEI':
                feature_importance = model.feature_importances_
                plt.figure(figsize=(8, 4))
                plt.bar(features, feature_importance)
                plt.title(f'Feature Importance for {index_type} Prediction at station {station}')
                plt.xlabel('Features')
                plt.ylabel('Importance')
                plt.tight_layout()
                plt.show()
                
                print(f"\nFeature Importance for {index_type} Prediction at station {station}:")
                for feature, importance in zip(features, feature_importance):
                    print(f"{feature}: {importance:.4f}")
        
        except Exception as e:
            print(f"An error occurred while processing {index_type} for station {station}: {str(e)}")
            continue