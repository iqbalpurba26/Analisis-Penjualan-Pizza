import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="ANALISIS PENJUALAN PIZZA",
    page_icon='assets/pizza.png'
)


def create_order_per_hari(df):
    order_per_hari_df = df.groupby(df['order_date'].dt.strftime(
        '%A')).order_id.count().sort_values(ascending=False)
    return order_per_hari_df


def create_order_per_bulan(df):
    order_per_bulan_df = df.groupby(df['order_date'].dt.strftime(
        '%B')).order_id.count().sort_values(ascending=False)
    return order_per_bulan_df


def create_pendapatan_per_bulan(df):
    pendapatan_bulan_df = df.groupby(
        df['order_date'].dt.strftime('%B')).total_price.sum()
    return pendapatan_bulan_df


def create_ukuran_pizza(df):
    ukuran_pizza_df = df.groupby(
        df['pizza_size']).quantity.sum().sort_values(ascending=False)
    return ukuran_pizza_df


def create_kategori_pizza(df):
    kategori_pizza_df = df.groupby(df['pizza_category']).quantity.sum()
    return kategori_pizza_df


def create_nama_pizza_df(df):
    nama_pizz_df = df.groupby(
        df['pizza_name']).quantity.sum().sort_values(ascending=False)
    return nama_pizz_df


all_df = pd.read_csv('pizza_sales_dataset.csv')
all_df['order_date'] = pd.to_datetime(all_df['order_date'])


min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()

with st.sidebar:
    st.image('assets/pizza.png')
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

main_df = all_df[(all_df["order_date"] >= start_date_str)
                 & (all_df["order_date"] <= end_date_str)]

main_df = all_df[(all_df["order_date"] >= str(start_date)) &
                 (all_df["order_date"] <= str(end_date))]

order_per_hari = create_order_per_hari(main_df)
order_per_bulan = create_order_per_bulan(main_df)
pendapatan_per_bulan = create_pendapatan_per_bulan(main_df)
ukuran_pizza = create_ukuran_pizza(main_df)
kategori_pizza = create_kategori_pizza(main_df)
nama_pizza = create_nama_pizza_df(main_df).head()

st.header("ANALISIS PENJUALAN PIZZA")
st.write('Analisis penjualan pizza dapat memberikan sejumlah manfaat bagi bisnis restoran atau toko pizza. Diantara manfaatnya itu adalah dapat mengoptimasi menu, pengelolaan persediaan, strategi harga, dan masih banyak lagi. Analisis penjualan pizza yang baik memberikan data yang menarik kepada suatu restoran. Untuk memudahkan proses penyampaian data, maka digunakanlah teknik visualisasi data.')

st.subheader("Perbandingan Penjualan Harian")
plt.figure(figsize=(20, 7))
sns.barplot(x=order_per_hari.index, y=order_per_hari.values)
plt.title("Total Order Harian", fontsize=20)
plt.xlabel("Hari", fontsize=20)
plt.ylabel("Total Pesanan", fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
st.pyplot(plt)

hari_tinggi = order_per_hari.index[0]
hari_terendah = order_per_hari.index[-1]
penjualan_tinggi = order_per_hari.iloc[0]
penjualan_terendah = order_per_hari.iloc[-1]

st.write(
    f"Dari hasil visualisasi data tersebut ditemukan bahwa, penjualan pizza tertinggi terjadi pada hari : **{hari_tinggi}** dengan total penjualan sebanyak **{penjualan_tinggi}**. Sedangkan penjualan pizza terendah terjadi pada hari **{hari_terendah}** dengan total penjualan sebanyak **{penjualan_terendah}**")


st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Perbandingan Penjualan Bulanan")
plt.figure(figsize=(20, 10))
sns.barplot(x=order_per_bulan.values, y=order_per_bulan.index)
plt.title("Total Order Bulanan", fontsize=20)
plt.xlabel("Total Pesanan ", fontsize=20)
plt.ylabel("Bulan", fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
st.pyplot(plt)

bulan_tinggi = order_per_bulan.index[0]
bulan_terendah = order_per_bulan.index[-1]
penjualan_bulan_tinggi = order_per_bulan.iloc[0]
penjualan_bulan_terendah = order_per_bulan.iloc[-1]

st.write(
    f"Dari hasil visualisasi data tersebut ditemukan bahwa, penjualan pizza tertinggi terjadi pada bulan : **{bulan_tinggi}** dengan total penjualan sebanyak **{penjualan_bulan_tinggi}**. Sedangkan penjualan pizza terendah terjadi pada bulan **{bulan_terendah}** dengan total penjualan sebanyak **{penjualan_bulan_terendah}**")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Pendapatan Per Bulan")
plt.figure(figsize=(20, 10))
plt.plot(pendapatan_per_bulan.index, pendapatan_per_bulan.values)
plt.title("Pendapatan Per Bulan", fontsize=20)
plt.xlabel("Bulan", fontsize=20)
plt.xticks(rotation=45)
plt.ylabel("USD", fontsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.grid(axis='y')
st.pyplot(plt)

analisis_pendapatan = pendapatan_per_bulan.sort_values(ascending=False)

bulan_pendapatan_tinggi = analisis_pendapatan.index[0]
bulan_pendapatan_terendah = analisis_pendapatan.index[-1]
pendapatan_bulan_tinggi = analisis_pendapatan.iloc[0]
pendapatan_bulan_terendah = analisis_pendapatan.iloc[-1]

st.write(
    f"Dari hasil visualisasi data tersebut ditemukan bahwa, pendapatan tertinggi dari penjualan pizza terjadi pada bulan **{bulan_pendapatan_tinggi}** dengan total pendapatan sebanyak **{pendapatan_bulan_tinggi} USD**. Sedangkan penjualan pizza terendah terjadi pada bulan **{bulan_pendapatan_terendah}** dengan total pendapatan sebanyak **{pendapatan_bulan_terendah} USD**")


st.markdown("<br>", unsafe_allow_html=True)

st.subheader('Perbandingan Penjualan Berdasarkan Ukuran Pizza')
plt.figure(figsize=(20, 10))
sns.barplot(x=ukuran_pizza.index, y=ukuran_pizza.values)
plt.title("Perbandingan Penjualan Berdasarkan Ukuran Pizza", fontsize=20)
plt.xlabel('Ukuran', fontsize=20)
plt.ylabel('Jumlah Pesanan', fontsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
st.pyplot(plt)


ukuran_terlaris = ukuran_pizza.index[0]
ukuran_kurang_laris = ukuran_pizza.index[-1]
total_penjualan_laris = ukuran_pizza.iloc[0]
total_penjualan_kurang = ukuran_pizza.iloc[-1]

st.write(
    f"Dari hasil visualisasi data tersebut ditemukan bahwa, ukuran pizza terlaris diduduki oleh ukuran **{ukuran_terlaris}** dengan total penjualan sebanyak **{total_penjualan_laris} buah**. Sedangkan ukuran pizza paling rendah penjualannnya yaitu ukuran **{ukuran_kurang_laris}** dengan total penjualan sebanyak **{total_penjualan_kurang} buah**")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader('Perbandingan Penjualan Berdasarkan Kategori Pizza')
fig, ax = plt.subplots(figsize=(20, 10))
pie = ax.pie(kategori_pizza.values,
             labels=kategori_pizza.index, autopct='%1.2f%%')
st.pyplot(fig)


kategori_terlaris = kategori_pizza.idxmax()
kategori_kurang_laris = kategori_pizza.idxmin()
total_kategori_laris = kategori_pizza.max()
total_kategori_kurang = kategori_pizza.min()

st.write(
    f"Dari hasil visualisasi data tersebut ditemukan bahwa, kategori pizza terlaris adalah kategori **{kategori_terlaris}** dengan total penjualan sebanyak **{total_kategori_laris} buah**. Sedangkan kateogri pizza paling rendah penjualannnya yaitu ukuran **{kategori_kurang_laris}** dengan total penjualan sebanyak **{total_kategori_kurang} buah**")

st.markdown("<br>", unsafe_allow_html=True)

st.subheader('Top 5 Pizza Terlaris')
plt.figure(figsize=(20, 10))
sns.barplot(x=nama_pizza.index, y=nama_pizza.head().values)
plt.title('5 Pizza Terlaris', fontsize=20)
plt.xlabel('Nama Pizza', fontsize=20)
plt.xticks(rotation=90)
plt.ylabel('Jumlah Pesanan', fontsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
st.pyplot(plt)

kategori_terlaris = nama_pizza.idxmax()
kategori_kurang_laris = nama_pizza.idxmin()
total_kategori_laris = nama_pizza.max()
total_kategori_kurang = nama_pizza.min()

st.write(
    f"Hasil visualisasi data diatas merupakan top 5 nama pizza terlaris dalam periode tertentu. Dari hasil visualisasi data tersebut ditemukan bahwa, nama pizza terlaris pada posisi pertama adalah **{kategori_terlaris}** dengan total penjualan sebanyak **{total_kategori_laris} buah**. Sedangkan pada posisi kelimad ditempati oleh **{kategori_kurang_laris}** dengan total penjualan sebanyak **{total_kategori_kurang} buah**")
