import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import utils

from datetime import timedelta

st.title('Dashboard Analisis Polusi Udara PM2.5 dan PM10 di Distrik Changping')
st.sidebar.header('Filter Data')

def load_data():
    df = pd.read_csv('dashboard/df_analysis.csv', index_col='Date')
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    return df

# Memuat data
df_analysis = load_data()

df_analysis.head()
df_analysis.info()

# Filter tanggal
min_date = df_analysis.index.min().date()
max_date = df_analysis.index.max().date()
start_date = st.sidebar.date_input('Tanggal Mulai', min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input('Tanggal Akhir', max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.sidebar.error("Tanggal Mulai tidak boleh lebih besar dari Tanggal Akhir")
else:
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date) + timedelta(days=1) - timedelta(seconds=1)
    filtered_df = df_analysis.loc[start_date:end_date]

    # Plot Pertanyaan 1
    st.subheader('Tren Tahunan PM2.5 dan PM10')
    annual_pm25 = filtered_df.resample('Y')['PM2.5'].mean()
    annual_pm10 = filtered_df.resample('Y')['PM10'].mean()
    fig, ax = plt.subplots(figsize=(15,10))
    sns.lineplot(x=annual_pm25.index.year, y=annual_pm25.values, marker='o', label='PM2.5', ax=ax)
    sns.lineplot(x=annual_pm10.index.year, y=annual_pm10.values, marker='s', label='PM10', ax=ax)
    ax.set_title('Tren Tahunan PM2.5 dan PM10')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Konsentrasi Rata-rata')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.subheader('Rata-rata Bulanan PM2.5 dan PM10')
    df_monthly = filtered_df.copy()
    df_monthly['month'] = filtered_df.index.month
    monthly_mean = df_monthly.groupby('month')[['PM2.5', 'PM10']].mean()
    fig, ax = plt.subplots(figsize=(15,10))
    monthly_mean.plot(kind='bar', ax=ax)
    ax.set_title('Rata-rata Bulanan PM2.5 dan PM10')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Konsentrasi Rata-rata')
    ax.set_xticks(range(12))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
    ax.grid(True)
    st.pyplot(fig)

    # Plot Pertanyaan 2
    st.subheader('Konsentrasi PM berdasarkan Arah Angin')
    wind_pm = filtered_df.groupby('wd')[['PM2.5', 'PM10']].mean()
    wind_pm.sort_values('PM2.5', ascending=False, inplace=True)
    fig, ax = plt.subplots(figsize=(15,10))
    wind_pm.plot(kind='bar', ax=ax)
    ax.set_title('Rata-rata PM2.5 dan PM10 berdasarkan Arah Angin')
    ax.set_xlabel('Arah Angin')
    ax.set_ylabel('Konsentrasi Rata-rata')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    # Plot Pertanyaan 3
    st.subheader('Persentase Hari Melebihi Standar WHO')
    WHO_THRESHOLD = 15

    df_daily = filtered_df.select_dtypes(exclude=['object']).resample('D').mean()
    df_daily['exceed'] = df_daily['PM2.5'] > WHO_THRESHOLD
    df_daily['year'] = df_daily.index.year
    annual_exceed_percent = df_daily.groupby('year')['exceed'].mean() * 100

    fig, ax = plt.subplots(figsize=(15,10))
    ax.annotate("Posisi Threshold WHO", xy=(0.01, 0.07), xycoords='axes fraction',
                 bbox=dict(boxstyle="round,pad=0.3", fc="lightgreen", alpha=0.3))
    ax.axhline(y=WHO_THRESHOLD, color='r', linestyle='--',)
    sns.lineplot(x=annual_exceed_percent.index, y=annual_exceed_percent.values, marker='o', ax=ax)
    ax.set_title('Persentase Hari dengan PM2.5 > 15 µg/m³ (WHO)')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Persentase Hari Melebihi Ambang (%)')
    ax.grid(True)
    st.pyplot(fig)

    df_analysis = utils.processing(df_analysis)

    # Plot Clustering 1
    st.subheader('Distribusi Kategori AQI PM2.5')

    cat_count = df_analysis['AQI_Category'].value_counts()[['Good','Moderate','Unhealthy for SG', 'Unhealthy', 'Very Unhealthy', 'Hazardous']]

    print(cat_count)

    fig, ax = plt.subplots(figsize=(15,10))

    sns.countplot(x='AQI_Category', data=df_analysis)
    ax.plot(cat_count, marker='o', color='red')
    ax.set_xlabel('Kategori AQI Index')
    ax.set_ylabel('Jumlah')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Plot Clustering 2
    st.subheader('PM2.5 Berdasarkan Waktu dan Kategori AQI')

    fig, ax = plt.subplots(figsize=(15,10))
    sns.scatterplot(x=df_analysis.index, y='PM2.5', hue='AQI_Category', data=df_analysis,
                    palette='viridis')
    ax.set_xlabel('Waktu')
    ax.set_ylabel('Konsentrasi PM2.5')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
