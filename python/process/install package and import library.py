# นี่คือขั้นตอนติดตั้ง package และ import library ที่จําเป็น
# Install Package And Import Library

!pip install pmdarima

!pip install tensorflow

!pip install geopandas

!pip install matplotlib

!pip install contextily

!pip install basemap

!pip install basemap-data-hires

!pip install climate_indices

!pip install xgboost

!pip install scikit-learn matplotlib

import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import norm
import os
import requests
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt 
%matplotlib inline
from datetime import datetime, timedelta
import geopandas as gpd
import contextily as ctx
from climate_indices import compute, indices
from scipy import stats
import matplotlib.dates as mdates
import xgboost as xgb
import csv

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

# Statsmodel libraries
from statsmodels.tsa.stattools import adfuller                 
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.statespace.sarimax import SARIMAX         
from statsmodels.tools.eval_measures import rmse
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA


# ARIMA
from pmdarima import auto_arima

# Sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# Keras
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# สร้างโฟลเดอร์สำหรับเก็บฟอนต์
font_dir = 'fonts'
os.makedirs(font_dir, exist_ok=True)

# ฟังก์ชันดาวน์โหลดฟอนต์
def download_font(url, font_name):
    response = requests.get(url)
    with open(os.path.join(font_dir, font_name), 'wb') as f:
        f.write(response.content)

# URL ของฟอนต์ Sarabun
font_urls = {
    'Sarabun-Regular.ttf': 'https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf',
    'Sarabun-Bold.ttf': 'https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf',
    'Sarabun-Italic.ttf': 'https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Italic.ttf',
    'Sarabun-BoldItalic.ttf': 'https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-BoldItalic.ttf'
}

# ดาวน์โหลดฟอนต์
for font_name, url in font_urls.items():
    download_font(url, font_name)

# เพิ่มฟอนต์ Sarabun ลงใน matplotlib
for font_name in font_urls.keys():
    fm.fontManager.addfont(os.path.join(font_dir, font_name))

# ตั้งค่าให้ฟอนต์เริ่มต้นเป็น Sarabun
plt.rcParams['font.family'] = 'Sarabun'

import warnings
warnings.filterwarnings("ignore")