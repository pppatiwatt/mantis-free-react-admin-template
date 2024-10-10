# นี่คือขั้นตอนเช็คข้อมูลเดือนและปีที่หายไป
# ข้อมูลเดือนและปีที่หายไป check missing years months

def check_missing_years_months(data):
    missing_data = []

    data['datetime'] = data['datetime'].dt.to_period('M')
    all_periods = pd.period_range(start=data['datetime'].min(), end=data['datetime'].max(), freq='M')

    for station in data['station'].unique():
        station_data = data[data['station'] == station]
        existing_periods = station_data['datetime'].unique()

        missing_periods = all_periods.difference(existing_periods)

        for period in missing_periods:
            missing_data.append((station, period))
    
    return missing_data

missing_humidity = check_missing_years_months(humidity)
missing_rainfall = check_missing_years_months(rainfall)
missing_temperature_max = check_missing_years_months(temperature_max)
missing_temperature_min = check_missing_years_months(temperature_min)
missing_evapotranspiration = check_missing_years_months(evapotranspiration)

def print_missing_data(missing_data, title):
    print(f"{title}:")
    if missing_data:
        for station, period in missing_data:
            print(f"สถานี: {station}, ปี/เดือน: {period}")
    else:
        print("ไม่มีปีและเดือนที่ขาดหายไป")

print_missing_data(missing_humidity, "ปีและเดือนที่ขาดหายไปในข้อมูล Humidity ( ความชื้นสัมพัทธ์ )")

print_missing_data(missing_rainfall, "ปีและเดือนที่ขาดหายไปในข้อมูล Rainfall ( ปริมาณน้ำฝน )")

print_missing_data(missing_temperature_max, "ปีและเดือนที่ขาดหายไปในข้อมูล Temperature max ( อุณหภูมิสูงสุด )")

print_missing_data(missing_temperature_min, "ปีและเดือนที่ขาดหายไปในข้อมูล Temperature min ( อุณหภูมิต่ำสุด )")

print_missing_data(missing_evapotranspiration, "ปีและเดือนที่ขาดหายไปในข้อมูล Evapotranspiration ( น้ำระเหยถาด )")