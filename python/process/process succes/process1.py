from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import io

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionResult(BaseModel):
    dates: List[str]
    actual_values: List[float]
    predictions: List[float]
    mse: float

def load_and_clean_data(file_content: bytes, data_type: str) -> pd.DataFrame:
    data = pd.read_csv(io.StringIO(file_content.decode('utf-8')), header=None)
    
    new_column_names = ['NO', 'STATION', 'DATETIME'] + [f'DAY{i}' for i in range(1, 32)] + ['TOTAL']
    data.columns = new_column_names

    if data_type == 'rainfall':
        data = data.rename(columns={'TOTAL': 'RAINFALL'})
        columns = ['NO', 'STATION', 'DATETIME', 'RAINFALL']
    elif data_type == 'evaporation':
        data = data.rename(columns={'TOTAL': 'EVAPORATION'})
        columns = ['STATION', 'DATETIME', 'EVAPORATION']
    elif data_type in ['temperature_max', 'temperature_min']:
        data = data.rename(columns={'TOTAL': 'AVERAGE'})
        columns = ['STATION', 'DATETIME', 'AVERAGE']
    
    data = data[columns]
    data['DATETIME'] = pd.to_datetime(data['DATETIME'], format='%b-%y', errors='coerce')
    data[columns[-1]] = pd.to_numeric(data[columns[-1]].replace(['T', '-'], np.nan), errors='coerce')
    data = data.dropna()
    
    return data

def process_data(rainfall: pd.DataFrame, evaporation: pd.DataFrame, temp_max: pd.DataFrame, temp_min: pd.DataFrame) -> PredictionResult:
    # Merge all data on DATETIME and STATION
    merged_data = rainfall.merge(evaporation, on=['DATETIME', 'STATION'])
    merged_data = merged_data.merge(temp_max, on=['DATETIME', 'STATION'], suffixes=('', '_max'))
    merged_data = merged_data.merge(temp_min, on=['DATETIME', 'STATION'], suffixes=('', '_min'))

    # Prepare features and target
    features = merged_data[['RAINFALL', 'EVAPORATION', 'AVERAGE', 'AVERAGE_min']]
    target = merged_data['RAINFALL']  # Assuming we're predicting rainfall

    # Split data into train and test sets
    train_size = int(0.8 * len(features))
    X_train, X_test = features[:train_size], features[train_size:]
    y_train, y_test = target[:train_size], target[train_size:]

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate MSE
    mse = mean_squared_error(y_test, predictions)

    # Prepare result
    result = PredictionResult(
        dates=merged_data['DATETIME'][train_size:].dt.strftime('%Y-%m-%d').tolist(),
        actual_values=y_test.tolist(),
        predictions=predictions.tolist(),
        mse=float(mse)
    )

    return result

@app.post("/upload-and-process/", response_model=PredictionResult)
async def upload_and_process(
    rainfall_file: UploadFile = File(...),
    evaporation_file: UploadFile = File(...),
    temperature_max_file: UploadFile = File(...),
    temperature_min_file: UploadFile = File(...)
):
    try:
        # Load and clean data
        rainfall_data = load_and_clean_data(await rainfall_file.read(), 'rainfall')
        evaporation_data = load_and_clean_data(await evaporation_file.read(), 'evaporation')
        temperature_max_data = load_and_clean_data(await temperature_max_file.read(), 'temperature_max')
        temperature_min_data = load_and_clean_data(await temperature_min_file.read(), 'temperature_min')

        # Process data and get results
        results = process_data(rainfall_data, evaporation_data, temperature_max_data, temperature_min_data)

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)