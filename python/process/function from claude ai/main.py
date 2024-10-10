from preprocess_data import preprocess_all_data
from calculate_indices import calculate_spei, calculate_spi
from train_models import train_random_forest_spei, train_random_forest_spi

def main():
    # Define file paths
    humidity_paths = [
        r"D:\project\Data\humid\humid-d-N-1-1998-2003.csv",
        r"D:\project\Data\humid\humid-d-N-2-1998-2003.csv",
        r"D:\project\Data\humid\humid-d-N-1-2004-2013.csv",
        r"D:\project\Data\humid\humid-d-N-2-2004-2013.csv",
        r"D:\project\Data\humid\humid-d-N-1-2014-2023.csv",
        r"D:\project\Data\humid\humid-d-N-2-2014-2023.csv"
    ]
    rainfall_paths = [
        r"D:\project\Data\Rain\Rain-N1-2003-1998.csv",
        r"D:\project\Data\Rain\Rain-N2-2003-1998.csv",
        r"D:\project\Data\Rain\Rain-N1-2013-2004.csv",
        r"D:\project\Data\Rain\Rain-N2-2013-2004.csv",
        r"D:\project\Data\Rain\Rain-N1-2023-2014.csv",
        r"D:\project\Data\Rain\Rain-N2-2023-2014.csv"
    ]
    temperature_max_paths = [
        r"D:\project\Data\MaxT\MaxT-N1-2003-1998.csv",
        r"D:\project\Data\MaxT\MaxT-N2-2003-1998.csv",
        r"D:\project\Data\MaxT\MaxT-N1-2013-2004.csv",
        r"D:\project\Data\MaxT\MaxT-N2-2013-2004.csv",
        r"D:\project\Data\MaxT\MaxT-N1-2023-2014.csv",
        r"D:\project\Data\MaxT\MaxT-N2-2023-2014.csv"
    ]
    temperature_min_paths = [
        r"D:\project\Data\MinT\MinT-N1-2003-1998.csv",
        r"D:\project\Data\MinT\MinT-N2-2003-1998.csv",
        r"D:\project\Data\MinT\MinT-N1-2013-2004.csv",
        r"D:\project\Data\MinT\MinT-N2-2013-2004.csv",
        r"D:\project\Data\MinT\MinT-N1-2023-2014.csv",
        r"D:\project\Data\MinT\MinT-N2-2023-2014.csv"
    ]
    evapotranspiration_paths = [
        r"D:\project\Data\eva\eva-d-N-1-1998-2003.csv",
        r"D:\project\Data\eva\eva-d-N-2-1998-2003.csv",
        r"D:\project\Data\eva\eva-d-N-1-2004-2013.csv",
        r"D:\project\Data\eva\eva-d-N-2-2004-2013.csv",
        r"D:\project\Data\eva\eva-d-N-1-2014-2023.csv",
        r"D:\project\Data\eva\eva-d-N-2-2014-2023.csv"
    ]

    # Preprocess data
    print("Preprocessing data...")
    humidity_data, rainfall_data, temperature_max_data, temperature_min_data, evapotranspiration_data = preprocess_all_data(
        humidity_paths, rainfall_paths, temperature_max_paths, temperature_min_paths, evapotranspiration_paths
    )

    # Calculate indices
    print("Calculating indices...")
    spei_results = calculate_spei(rainfall_data, evapotranspiration_data, temperature_max_data, temperature_min_data)
    spi_results = calculate_spi(rainfall_data)

    # Train models and make predictions
    print("Training models and making predictions...")
    spei_predictions = train_random_forest_spei(spei_results)
    spi_predictions = train_random_forest_spi(spi_results)

    # Save results
    spei_predictions.to_csv('predicted_spei_results.csv', index=False, encoding='utf-8')
    spi_predictions.to_csv('predicted_spi_results.csv', index=False, encoding='utf-8')
    print("Results have been saved to 'predicted_spei_results.csv' and 'predicted_spi_results.csv'")

if __name__ == "__main__":
    main()