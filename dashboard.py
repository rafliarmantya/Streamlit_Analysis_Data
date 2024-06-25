import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Reading datasets in CSV format
day_df = pd.read_csv('day.csv')
day_df.head()
hour_df = pd.read_csv('hour.csv')
hour_df.head()
all_df = pd.read_csv("all_data.csv")

# Change the data type if necessary, for example date
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Added 'season_name' column for more readable season names
season = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_name'] = day_df['season'].map(season)
hour_df['season_name'] = hour_df['season'].map(season)

# Added 'weekday_name' column for more readable weekday names
weekday = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
day_df['weekday_name'] = day_df['weekday'].map(weekday)
hour_df['weekday_name'] = hour_df['weekday'].map(weekday)

# Added a column for easier to read weather conditions
weather = {1: 'Clear', 2: 'Cloudy/Misty', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
day_df['weather_name'] = day_df['weathersit'].map(weather)
hour_df['weather_name'] = hour_df['weathersit'].map(weather)

day_df.groupby(by="season_name").season.nunique().sort_values(ascending=False)
day_df.groupby(by="weather_name").weathersit.nunique().sort_values(ascending=False)
hour_df.groupby(by="season_name").season.nunique().sort_values(ascending=False)
hour_df.groupby(by="weather_name").weathersit.nunique().sort_values(ascending=False)


all_df = pd.merge(
    left=day_df,
    right=hour_df,
    how="outer",
    )
all_df.head()


# Fungsi untuk memuat data
@st.cache_data
def load_data():
    all_df = pd.read_csv('all_data.csv')
    day_df = pd.read_csv('day.csv')
    hour_df = pd.read_csv('hour.csv')
    all_df['dteday'] = pd.to_datetime(all_df['dteday'])
    day_df = all_df.groupby('dteday').agg({'cnt': 'sum'}).reset_index()
    hour_df = all_df.copy()
    return all_df, day_df, hour_df

# Memuat data
all_df, day_df, hour_df = load_data()

# Judul dashboard
st.title('Dashboard Sharing Bike🚲')

# Widget untuk memilih rentang tanggal
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start Date', min(all_df['dteday']).date())
with col2:
    end_date = st.date_input('End Date', max(all_df['dteday']).date())

# Memfilter data berdasarkan rentang tanggal yang dipilih
filtered_df = all_df[(all_df['dteday'].dt.date >= start_date) & 
                     (all_df['dteday'].dt.date <= end_date)]

# Menampilkan informasi data yang difilter
st.write(f"Data dari {start_date} hingga {end_date}")
st.write(f"Jumlah baris data: {len(filtered_df)}")

# Visualisasi jumlah penyewaan sepeda per hari
st.subheader('Total Data Jumlah Penyewaan Sepeda per Hari dan Jam')
daily_rentals = filtered_df.groupby(filtered_df['dteday'].dt.date)['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_rentals['dteday'], daily_rentals['cnt'])
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Visualisasi distribusi penyewaan berdasarkan hari dalam seminggu
st.subheader('Distribusi Penyewaan Berdasarkan Hari dalam Seminggu')
filtered_df['day_of_week'] = filtered_df['dteday'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='day_of_week', y='cnt', data=filtered_df, order=day_order, ax=ax)
ax.set_xlabel('Hari')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Statistik ringkasan
st.subheader('Statistik Ringkasan')
st.write(filtered_df['cnt'].describe())

# Menampilkan data mentah
if st.checkbox('Tampilkan Data Mentah'):
    st.subheader('Data Mentah')
    st.write(filtered_df)

all_df.season_name.hist()
all_df.weather_name.hist()


# Merge Total season_name

from matplotlib import pyplot as plt
import seaborn as sns
all_df.groupby('season_name').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

# Merge Total weather_name

from matplotlib import pyplot as plt
import seaborn as sns
all_df.groupby('weather_name').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

# Distribusi Musim dan Cuaca
st.subheader('Distribusi Musim dan Cuaca')
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    all_df['season_name'].hist(ax=ax)
    ax.set_title('Distribusi Musim')
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    all_df['weather_name'].hist(ax=ax)
    ax.set_title('Distribusi Cuaca')
    st.pyplot(fig)


# Total penyewaan berdasarkan musim
st.subheader('Total Penyewaan Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(10, 6))
all_df.groupby('season_name').size().plot(kind='barh', ax=ax, color=sns.color_palette('Dark2'))
ax.spines[['top', 'right']].set_visible(False)
ax.set_title('Total Penyewaan per Musim')
st.pyplot(fig)

# Total penyewaan berdasarkan cuaca
st.subheader('Total Penyewaan Berdasarkan Cuaca')
fig, ax = plt.subplots(figsize=(10, 6))
all_df.groupby('weather_name').size().plot(kind='barh', ax=ax, color=sns.color_palette('Dark2'))
ax.spines[['top', 'right']].set_visible(False)
ax.set_title('Total Penyewaan per Kondisi Cuaca')
st.pyplot(fig)




# Mengelompokkan data berdasarkan musim
grouped_data = all_df.groupby(by=["season_name"]).agg({
    "workingday": "sum",
    "casual": "sum"
})

# Menghitung rata-rata penyewa casual per hari kerja
grouped_data['casual_per_workday'] = grouped_data['casual'] / grouped_data['workingday']

# Membuat bar plot
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(grouped_data.index, grouped_data['casual_per_workday'], 
              color=['#FFA07A', '#98FB98', '#DEB887', '#87CEFA'])

# Menambahkan label dan judul
ax.set_xlabel('Musim', fontsize=12)
ax.set_ylabel('Rata-rata Penyewa Casual per Hari Kerja', fontsize=12)
ax.set_title('Perbandingan Rata-rata Penyewa Casual per Hari Kerja Antar Musim', fontsize=14)

# Menambahkan nilai di atas setiap bar
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}',
            ha='center', va='bottom', fontsize=10)

# Menyesuaikan tampilan
plt.xticks(rotation=0, fontsize=10)
plt.yticks(fontsize=10)

# Menambahkan grid untuk memudahkan pembacaan
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menampilkan data dalam bentuk tabel
st.subheader('Data Penyewaan Sepeda Casual per Hari Kerja')
st.write(grouped_data)

# Analisis tambahan
summer_casual = grouped_data.loc['Summer', 'casual_per_workday']
winter_casual = grouped_data.loc['Winter', 'casual_per_workday']
percentage_difference = ((summer_casual - winter_casual) / winter_casual) * 100

st.subheader('Analisis Musim Panas vs Musim Dingin')
col1, col2 = st.columns(2)
with col1:
    st.metric("Rata-rata penyewa casual per hari kerja di musim panas", f"{summer_casual:.2f}")
    st.metric("Rata-rata penyewa casual per hari kerja di musim dingin", f"{winter_casual:.2f}")
with col2:
    st.metric("Persentase penurunan", f"{abs(percentage_difference):.2f}%", 
              delta=f"-{abs(percentage_difference):.2f}%", delta_color="inverse")
    

# Mengelompokkan data berdasarkan cuaca dan menghitung total registered
weather_data = all_df.groupby(by=["weather_name"]).agg({
    "registered": "sum"
}).reset_index()

# Memfilter hanya untuk cuaca cerah dan mendung berawan
weather_data = weather_data[weather_data['weather_name'].isin(['Clear', 'Cloudy/Misty'])]

st.title("Analisis Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
st.write("""
Dashboard ini menunjukkan perbandingan total penyewaan sepeda oleh pengguna terdaftar
berdasarkan kondisi cuaca (cerah dan mendung berawan).
""")

# Check if there is data for 'Cloudy/Misty' weather
if 'Cloudy/Misty' in weather_data['weather_name'].values:
    # Membuat bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weather_name', y='registered', data=weather_data, 
                palette=['#FFA07A', '#87CEFA'], ax=ax)

    # Menambahkan label dan judul
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Total Sepeda Disewa (Registered)', fontsize=12)
    ax.set_title('Perbandingan Total Sepeda Disewa oleh Pengguna Registered\nBerdasarkan Kondisi Cuaca', fontsize=14)

    # Menambahkan nilai di atas setiap bar
    for i, v in enumerate(weather_data['registered']):
        ax.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

    # Menyesuaikan tampilan
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

    # Menambahkan grid untuk memudahkan pembacaan
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    # Mencetak data untuk verifikasi
    st.write("Data Terfilter Berdasarkan Kondisi Cuaca:")
    st.dataframe(weather_data)

    # Analisis tambahan
    clear_total = weather_data[weather_data['weather_name'] == 'Clear']['registered'].values[0]
    cloudy_total = weather_data[weather_data['weather_name'] == 'Cloudy/Misty']['registered'].values[0]
    percentage_difference = ((clear_total - cloudy_total) / cloudy_total) * 100

    st.write(f"\nTotal sepeda disewa saat cuaca cerah: {clear_total:.2f}")
    st.write(f"Total sepeda disewa saat cuaca mendung berawan: {cloudy_total:.2f}")
    st.write(f"Persentase perbedaan: {percentage_difference:.2f}%")
else:
    st.write("Tidak ada data untuk kondisi cuaca 'Cloudy/Misty'")
