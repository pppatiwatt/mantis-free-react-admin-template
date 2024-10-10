import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def train_random_forest_spei(all_spei_results):
    all_spei_results['datetime'] = pd.to_datetime(all_spei_results['datetime'])
    
    train_data = all_spei_results[all_spei_results['datetime'].dt.year <= 2022]
    test_data = all_spei_results[all_spei_results['datetime'].dt.year == 2023]

    train_data = train_data.fillna(method='ffill')
    test_data = test_data.fillna(method='ffill')

    stations = all_spei_results['station'].unique()

    predicted_spei_results_RandomForest = pd.DataFrame(columns=['datetime', 'station', 'actual_spei', 'predicted_spei'])

    for station in stations:
        train_station = train_data[train_data['station'] == station]
        test_station = test_data[test_data['station'] == station]

        if test_station.empty:
            print(f"No data available for 2023 at station {station}. Skipping this station.")
            continue

        X_train_station = train_station[['pet', 'w']]
        y_train_station = train_station['spei']
        X_test_station = test_station[['pet', 'w']]
        y_test_station = test_station['spei']

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_station, y_train_station)

        RandomForest_spei_2023 = model.predict(X_test_station)

        mse = mean_squared_error(y_test_station, RandomForest_spei_2023)
        print(f"Station: {station}, Mean Squared Error for 2023: {mse}")

        station_results = pd.DataFrame({
            'datetime': test_station['datetime'],
            'station': station,
            'actual_spei': y_test_station,
            'predicted_spei': RandomForest_spei_2023
        })
        predicted_spei_results_RandomForest = pd.concat([predicted_spei_results_RandomForest, station_results], ignore_index=True)

        plt.figure(figsize=(12, 6))
        plt.plot(test_station['datetime'], y_test_station, label='Actual SPEI 2023', marker='o')
        plt.plot(test_station['datetime'], RandomForest_spei_2023, label='Predicted SPEI 2023', marker='x')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('SPEI')
        plt.title(f'Station: {station} - Actual vs Predicted SPEI for 2023 (Random Forest)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        print(f"\nPredicted vs Actual SPEI for 2023 at station {station}:")
        for date, prediction, actual in zip(test_station['datetime'], RandomForest_spei_2023, y_test_station):
            print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}, Actual: {actual:.4f}")

        test_station['Quarter'] = test_station['datetime'].dt.to_period('Q')
        test_station['RandomForest_Predicted_SPEI'] = RandomForest_spei_2023
        RandomForest_Quarterly_spei_2023 = test_station.groupby('Quarter').agg({
            'spei': 'mean',
            'RandomForest_Predicted_SPEI': 'mean'
        }).rename(columns={'spei': 'Actual', 'RandomForest_Predicted_SPEI': 'Predicted'})

        plt.figure(figsize=(10, 5))
        RandomForest_Quarterly_spei_2023[['Actual', 'Predicted']].plot(kind='bar', position=1, width=0.4, label=['Actual SPEI', 'Predicted SPEI'])
        plt.legend()
        plt.xlabel('Quarter')
        plt.ylabel('Average SPEI')
        plt.title(f'Station: {station} - Quarterly Average SPEI for 2023 (Random Forest)')
        plt.tight_layout()
        plt.show()

        print(f"\nQuarterly Average SPEI for 2023 at station {station}:")
        for quarter, row in RandomForest_Quarterly_spei_2023.iterrows():
            print(f"{quarter}: Actual: {row['Actual']:.4f}, Predicted: {row['Predicted']:.4f}")

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

    return predicted_spei_results_RandomForest

def train_random_forest_spi(all_spi):
    all_spi['datetime'] = pd.to_datetime(all_spi['datetime'])

    train_data = all_spi[all_spi['datetime'].dt.year <= 2022]
    test_data = all_spi[all_spi['datetime'].dt.year == 2023]

    train_data = train_data.fillna(method='ffill')
    test_data = test_data.fillna(method='ffill')

    stations = all_spi['station'].unique()

    predicted_spi_results_RandomForest = pd.DataFrame(columns=['datetime', 'station', 'actual_spi', 'predicted_spi'])

    for station in stations:
        train_station = train_data[train_data['station'] == station]
        test_station = test_data[test_data['station'] == station]

        if test_station.empty:
            print(f"No data available for 2023 at station {station}. Skipping this station.")
            continue

        X_train_station = train_station[['spi']]
        y_train_station = train_station['spi']
        X_test_station = test_station[['spi']]
        y_test_station = test_station['spi']

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_station, y_train_station)

        RandomForest_spi_2023 = model.predict(X_test_station)

        mse = mean_squared_error(y_test_station, RandomForest_spi_2023)
        print(f"Station: {station}, Mean Squared Error for SPI prediction in 2023: {mse}")

        plt.figure(figsize=(12, 6))
        plt.plot(test_station['datetime'], y_test_station, label='Actual SPI 2023', marker='o')
        plt.plot(test_station['datetime'], RandomForest_spi_2023, label='Predicted SPI 2023', marker='x')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('SPI')
        plt.title(f'Station: {station} - Actual vs Predicted SPI for 2023')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        print(f"\nPredicted vs Actual SPI for 2023 at station {station}:")
        for date, prediction, actual in zip(test_station['datetime'], RandomForest_spi_2023, y_test_station):
            print(f"{date.strftime('%Y-%m')}: Predicted: {prediction:.4f}, Actual: {actual:.4f}")

        station_results = pd.DataFrame({
            'datetime': test_station['datetime'],
            'station': station,
            'actual_spi': y_test_station,
            'predicted_spi': RandomForest_spi_2023
        })
        predicted_spi_results_RandomForest = pd.concat([predicted_spi_results_RandomForest, station_results], ignore_index=True)

        test_station['Quarter'] = test_station['datetime'].dt.to_period('Q')
        test_station['RandomForest_Predicted_SPI'] = RandomForest_spi_2023
        quarterly_data = test_station.groupby('Quarter').agg({
            'spi': 'mean',
            'RandomForest_Predicted_SPI': 'mean'
        }).rename(columns={'spi': 'Actual_SPI', 'RandomForest_Predicted_SPI': 'Predicted_SPI'})

        print(f"\nQuarterly Average SPI for 2023 at station {station}:")
        for quarter, row in quarterly_data.iterrows():
            print(f"{quarter}: Actual SPI: {row['Actual_SPI']:.4f}, Predicted SPI: {row['Predicted_SPI']:.4f}")

    return predicted_spi_results_RandomForest