import math
import pandas as pd

def linear(AQIhigh, AQIlow, Conchigh, Conclow, concentration):
    conc = float(concentration)
    a = ((conc - Conclow) / (Conchigh - Conclow)) * (AQIhigh - AQIlow) + AQIlow
    return round(a)

def aqi_pm25(concentration):
    c = math.floor(10 * float(concentration)) / 10.0
    if 0.0 <= c <= 9.0:
        return linear(50, 0, 9.0, 0.0, c)
    elif 9.1 <= c <= 35.4:
        return linear(100, 51, 35.4, 9.1, c)
    elif 35.5 <= c <= 55.4:
        return linear(150, 101, 55.4, 35.5, c)
    elif 55.5 <= c <= 125.4:
        return linear(200, 151, 125.4, 55.4, c)
    elif 125.5 <= c <= 225.4:
        return linear(300, 201, 225.4, 125.5, c)
    elif c >= 225.5:
        return linear(500, 301, 325.4, 225.5, c)
    else:
        return "Out of Range"

def aqi_cat(aqi):
    """
    Skor didasarkan pada tabel yang ada di web https://aqicn.org/scale/

    Skor M (Magnitude) berdasarkan nilai AQI:
      AQI <= 50   => skor 1 (Good)
      AQI <= 100  => skor 2 (Moderate)
      AQI <= 150  => skor 3 (Unhealthy for Sensitive Groups)
      AQI <= 200  => skor 4 (Unhealthy)
      AQI <= 300  => skor 5 (Very Unhealthy)
      AQI > 300   => skor 6 (Hazardous)
    """
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for SG"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def health_risk_category(pm25):
    if pm25 <= 5:
        return "Minimal Risk"
    elif pm25 <= 10:
        return "Low Risk"
    elif pm25 <= 20:
        return "Medium Risk"
    elif pm25 <= 35:
        return "High Risk"
    else:
        return "Very High Risk"

def processing(df):
    df['AQI_PM25'] = df['PM2.5'].apply(aqi_pm25)
    df['AQI_Category'] = df['AQI_PM25'].apply(aqi_cat)
    
    pm25_min = df['PM2.5'].min()
    pm25_max = df['PM2.5'].max()
    bin_width = (pm25_max - pm25_min) / 5
    
    bins = [pm25_min + i * bin_width for i in range(6)]
    labels = [f'Bin {i+1}' for i in range(5)]
    df['PM25_EqualWidth_Bin'] = pd.cut(df['PM2.5'], bins=bins, labels=labels, include_lowest=True)
    
    df['PM25_EqualFreq_Bin'] = pd.qcut(df['PM2.5'], q=5, labels=[f'Quantile {i+1}' for i in range(5)], duplicates='drop')
    
    df['Health_Risk'] = df['PM2.5'].apply(health_risk_category)
    
    return df