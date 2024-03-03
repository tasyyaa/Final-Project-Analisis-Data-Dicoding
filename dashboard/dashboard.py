import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_monthly_data(df):
    df.set_index('dteday', inplace=True)
    monthly_data = df.resample('M').sum()
    return monthly_data

def create_total_sewa(df):
    df['yr'] = df['yr_x'].replace({0: '2011', 1: '2012'})
    total_sewa = df.groupby(by="yr_x").cnt_x.sum()
    return total_sewa

def create_cnt_daily(df):
    cnt_daily = df.groupby(by="dteday").cnt_y.sum()
    return cnt_daily

def create_casual_daily(df):
    casual_daily = df.groupby(by="dteday").casual_y.sum()
    return casual_daily

def create_regist_daily(df):
    regist_daily = df.groupby(by="dteday").registered_y.sum()
    return regist_daily

def create_hourly_hour_sum(df):
    hourly_all_sum = df.groupby(by="hr").cnt_y.sum()
    return hourly_all_sum

def create_jumlah_weekday(df):
    df['weekday_x'] = df['weekday_x'].replace({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"})
    jumlah_weekday = df.groupby(by="weekday_x")['cnt_x'].sum()
    return jumlah_weekday

def create_perbandingan_holiday(df):
    jumlah_penyewaan = df.groupby(by="holiday_x").cnt_x.sum()
    jumlah_hari = df.groupby(by="holiday_x").instant_x.count()
    perbandingan_holiday = jumlah_penyewaan / jumlah_hari
    perbandingan_holiday_sorted = perbandingan_holiday.sort_values(ascending=False)
    return perbandingan_holiday_sorted

def create_temp_daily(df):
    temp_daily = df.groupby(by="dteday").temp_x.mean()
    temp_daily = temp_daily *41
    return temp_daily

def create_all_data(df):
    all_data_df = df
    return all_data_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
with st.sidebar:
    st.image("Bike Sharing.png", use_column_width=True)
    start_date, end_date = st.date_input(
        label='Tanggal Peminjaman',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

monthly_data = create_monthly_data(main_df)
total_sewa = create_total_sewa(main_df)
cnt_daily = create_cnt_daily(main_df)
casual_daily = create_casual_daily(main_df)
regist_daily = create_regist_daily(main_df)
hourly_all_sum = create_hourly_hour_sum(main_df)
jumlah_weekday = create_jumlah_weekday(main_df)
perbandingan_holiday_sorted = create_perbandingan_holiday(main_df)
temp_daily = create_temp_daily(main_df)
all_data_df = create_all_data(main_df)


st.header('Bike Sharing 2011-2012 Dashboard :')

st.subheader(f"Summary {start_date} until {end_date}")

col1, col2, col3 = st.columns(3)
 
with col1:
    st.metric("Temperature", value=temp_daily.mean().round(2))

with col2:
    cnt_total =  cnt_daily
    st.metric("Total Sharing", value=cnt_daily.sum())
 
with col3:
    holiday_ses = all_df['holiday_x'].iloc[0]
    st.metric("Season", value=holiday_ses)


st.subheader("Bike Sharing Count per Hour")
all_hours = np.arange(24)
hourly_all_sum = hourly_all_sum.reindex(all_hours, fill_value=0)
idx_max = np.argmax(hourly_all_sum.values)
colors = ['blue' if i != idx_max else 'green' for i in range(len(hourly_all_sum))]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(hourly_all_sum.index, hourly_all_sum.values, marker='o',markersize=2, linestyle='-')
ax.plot(hourly_all_sum.index[idx_max], hourly_all_sum.values[idx_max], marker='o', markersize=8, linestyle='None', color='green')
ax.set_xlabel('Hour')
ax.set_ylabel('Bike Sharing Count')
ax.set_title('Bike Sharing Count per Hour')
ax.set_xticks(hourly_all_sum.index)
ax.grid(True)
st.pyplot(fig)

st.subheader("Distribution of Count by Hour")
plt.figure(figsize=(10, 6))
sns.boxplot(x='hr', y='cnt_y', data=all_data_df)
plt.title('Box Plot: Sum of Bike Sharing Per Hour')
plt.xlabel('Hour')
plt.ylabel('Bike Sharing per Hour')
st.pyplot(plt)

st.subheader("Bike Sharing Count by day")
col1, col2 = st.columns(2)
with col1:
    jumlah_weekday_sorted = jumlah_weekday.sort_values(ascending=False)
    weekday_min = jumlah_weekday_sorted.min()
    weekday_max = jumlah_weekday_sorted.max()
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_ = ['red' if val == weekday_min else 'green' if val == weekday_max else '#D3D3D3' for val in jumlah_weekday_sorted.values]
    sns.barplot(
        x=jumlah_weekday.values,
        y=jumlah_weekday.index,
        order=jumlah_weekday_sorted.index,
        palette=colors_,
        ax=ax
    )
    ax.set_title("Bike Sharing Count by Day", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

with col2:
    weekday_max = np.argmax(jumlah_weekday.values)
    weekday_min = np.argmin(jumlah_weekday.values)
    colors = ['lightgrey' if i != weekday_max else 'green' for i in range(len(jumlah_weekday))]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(jumlah_weekday.index, jumlah_weekday.values, marker='o',markersize=2, linestyle='-')
    ax.plot(jumlah_weekday.index[weekday_max], jumlah_weekday.values[weekday_max], marker='o', markersize=8, linestyle='None', color='green')
    ax.plot(jumlah_weekday.index[weekday_min], jumlah_weekday.values[weekday_min], marker='o', markersize=8, linestyle='None', color='red')
    ax.set_xlabel('Day')
    ax.set_ylabel('Bike Sharing Count')
    ax.set_title('Bike Sharing Count by Day')
    ax.set_xticks(jumlah_weekday.index)
    ax.grid(True)
    st.pyplot(fig)


st.subheader("Impact of Holiday in Bike Sharing Count")
col1, col2, col3 = st.columns(3)
with col1:
    fig, ax = plt.subplots()
    ax.pie(perbandingan_holiday_sorted.values, labels=perbandingan_holiday_sorted.index, autopct='%1.1f%%', startangle=90, colors=['green', 'lightgrey'])
    ax.axis('equal')  # Agar pie chart terlihat lingkaran
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots()
    perbandingan_holiday_sorted.plot(kind='bar', ax=ax, color=['green', 'lightgrey'])
    ax.set_ylabel('Bike Sharing Count')
    ax.set_xlabel('Holiday Status')
    ax.set_title('Comparison of Bike Rental Counts on Holidays and Regular Days')
    st.pyplot(fig)

with col3:
    all_data_df['holiday_x'] = all_data_df['holiday_x'].replace({'not holiday': 0, 'holiday': 1})
    correlation = all_data_df[['cnt_x', 'holiday_x']].corr()
    st.write("Corelation between holiday and cnt:", correlation)

st.subheader("Bike Sharing Growth 2011-2012")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    total_sewa.plot(kind='bar', ax=ax, color=['lightgrey', 'green'])
    ax.set_ylabel('Bike Sharing Count')
    ax.set_xlabel('Year')
    ax.set_title('Comparison of Bike Rental Counts in 2011 and 2012')
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(monthly_data.index, monthly_data['cnt_x'], marker='o', linestyle='-')
    ax.set_xlabel('Month')
    ax.set_ylabel('Bike Sharing Count')
    ax.set_title('Bike Sharing Count per month')
    ax.grid(True)
    st.pyplot(fig)