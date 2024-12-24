import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import plotly.express as px

# Membaca data dari file CSV
df = pd.read_csv('scraped_sv_product_data.csv')
keywords_df = pd.read_csv('brand_and_gadget_keywords.csv')

# Mengonversi kolom tanggal ke format datetime
df['Tanggal Post'] = pd.to_datetime(df['Tanggal Post'])

# Membuat list kata kunci dari dataframe keywords
keywords = keywords_df['Brand'].tolist()

# Daftar kata kunci non-elektronik
non_electronic_keywords = [
    'Stiker', 'Isolasi', 'Lakban', 'Tape', 'Penambal', 'Lubang', 'Bolong', 
    'Jaring', 'Kawat', 'Nyamuk', 'Jendela', 'Pintu', 'Sunlight', 'Biocare', 
    'Nature', 'Zwitsal', 'DURALEX', 'PLATE', 'Piring', 'Makan', 'Kaca', 'Glass', 
    'Dinner', 'Dessert','Cuka Apel Gemeli Premium 500ml With Mother','UNITWO [BED COVER+SPREI SET] Bed Cover Set Dengan Sprei Set, Sarung Bantal dan Sarung Guling Full Pressing Karet Keliling Lembut Motif Polos - Seprei Set Polos Korea Lembut','Systema Sikat Gigi Smart Clean Isi 3 Pcs','Smart Breast Mask - Masker Pembesar & Pengencang Payudara','Celengan Target Delano Smart Saver Thumbler Viral / Souvenir Ulang Tahun Murah Celengan Koin Bisa Buka Tutup','PASEO - Tissue Smart Facial 250 Sheets 2 Ply','Soklin Smart Deterjen Bubuk Soft 725 gr',
    'KUKE Isi Ulang Lem Tembak eagle brand/ Reffil LeTembak / Lem Bakar Kecil / Reffil Glue Gun Kecil 7mm',
    'OMG OH MY GLAM Mattelast Lip Cream 2.9 g - Lip Cream Matte Dengan Warna Intense, Tahan Lama & Ringan',
'OIL POT OILPOT Saringan Minyak Goreng Stainless Steel 1,3 1.3 L Sisa Wadah Jelantah Wadah Anti Karat Stainles 1,3L 1.3L 1300ml 1300 mL Filter Gelas Mug Tempat',
'ALGAN25 KIPAS ANGIN TANGAN BULAT LIPAT AJAIB MOTIF KARAKTER KARTUN LUCU KIPAS PORTABLE MINI VIRAL']

# Fungsi untuk memfilter produk berdasarkan kata kunci elektronik, non-elektronik, dan brand
def filter_products(df, keywords, non_electronic_keywords):
    # Filter berdasarkan kata kunci elektronik
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['Nama Produk'])
    keywords_matrix = vectorizer.transform([' '.join(keywords)])
    
    cosine_similarities = cosine_similarity(tfidf_matrix, keywords_matrix).flatten()
    df['Similarity'] = cosine_similarities
    df_filtered = df[df['Similarity'] > 0]  # Threshold for similarity
    
    # Filter berdasarkan kata kunci non-elektronik
    non_electronic_filter = df_filtered['Nama Produk'].apply(
        lambda x: not any(kw.lower() in x.lower() for kw in non_electronic_keywords)
    )
    df_filtered = df_filtered[non_electronic_filter]
    
    # Filter berdasarkan brand keywords
    brand_filter = df_filtered['Nama Produk'].apply(
        lambda x: any(brand.lower() in x.lower() for brand in keywords)
    )
    df_filtered = df_filtered[brand_filter]
    
    return df_filtered

# Fungsi untuk menghitung interaksi selama n hari terakhir
def top_products_last_n_days(df, days):
    end_date = df['Tanggal Post'].max()
    start_date = end_date - pd.Timedelta(days=days)
    
    df_last_n_days = df[(df['Tanggal Post'] >= start_date) & (df['Tanggal Post'] <= end_date)]
    df_filtered = filter_products(df_last_n_days, keywords, non_electronic_keywords)

    product_stats = df_filtered.groupby('Nama Produk').agg({
        'Jumlah Komentar': 'sum',
        'Jumlah Like': 'sum',
        'Jumlah View': 'sum'
    }).reset_index()

    product_stats['Total Interaksi'] = product_stats['Jumlah Komentar'] + product_stats['Jumlah Like'] + product_stats['Jumlah View']
    
    top_products = product_stats.sort_values(by='Total Interaksi', ascending=False).head(10)
    
    return top_products

# Menampilkan 10 produk teratas selama 30, 15, dan 7 hari terakhir
top_products_30_days = top_products_last_n_days(df, 30)
top_products_15_days = top_products_last_n_days(df, 15)
top_products_7_days = top_products_last_n_days(df, 7)

def plot_top_products(top_products, title):
    fig = px.bar(top_products, 
                 x='Total Interaksi', 
                 y='Nama Produk', 
                 orientation='h', 
                 hover_data=['Jumlah Komentar', 'Jumlah Like', 'Jumlah View'], 
                 color='Total Interaksi', 
                 color_continuous_scale='Viridis',
                 labels={'Total Interaksi': 'Total Interaksi', 'Nama Produk': 'Nama Produk'},
                 height=600)
    fig.update_layout(title_text=title, title_x=0.5, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)

# Judul aplikasi
st.title('Analisis Interaksi Produk')

# Menampilkan visualisasi untuk 10 produk teratas
st.header('10 Produk Teratas Berdasarkan Total Interaksi')
plot_top_products(top_products_30_days, '30 Hari Terakhir')
plot_top_products(top_products_15_days, '15 Hari Terakhir')
plot_top_products(top_products_7_days, '7 Hari Terakhir')

# Mengambil nama produk dari setiap DataFrame
produk_30_hari = set(top_products_30_days['Nama Produk'])
produk_15_hari = set(top_products_15_days['Nama Produk'])
produk_7_hari = set(top_products_7_days['Nama Produk'])

# Menggunakan operasi union untuk mendapatkan produk yang muncul di salah satu daftar
produk_common = produk_30_hari.union(produk_15_hari, produk_7_hari)

# Menampilkan produk yang muncul di semua daftar
st.subheader('Produk yang Muncul di Top 10 untuk 30, 15, dan 7 Hari Terakhir:')
for product in produk_common:
    st.markdown(f"- [{product}](URL_OF_{product.replace(' ', '_')})")

# Filter data untuk produk yang muncul di semua daftar
common_products_df = df[df['Nama Produk'].isin(produk_common)]

# Plot jumlah promotor untuk produk yang muncul di semua daftar
def plot_competition(common_products_df):
    competition_stats = common_products_df.groupby('Nama Produk').agg({
        'User Name': 'nunique'  # Menghitung jumlah promotor unik
    }).reset_index()

    competition_stats = competition_stats.rename(columns={'User Name': 'Jumlah Promotor'})

    fig = px.bar(competition_stats, 
                 x='Nama Produk', 
                 y='Jumlah Promotor', 
                 color='Jumlah Promotor', 
                 color_continuous_scale='Bluered', 
                 labels={'Jumlah Promotor': 'Jumlah Promotor', 'Nama Produk': 'Nama Produk'},
                 height=600)
    fig.update_layout(title_text='Tingkat Persaingan (Jumlah Promotor)', title_x=0.5, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)

# Menampilkan visualisasi tingkat persaingan
st.subheader('Tingkat Persaingan untuk Produk yang Muncul di Daftar 30, 15, dan 7 Hari Terakhir')
plot_competition(common_products_df)

# Rekomendasi berdasarkan analisis
st.subheader('Rekomendasi Berdasarkan Analisis:')
rekomendasi = """
1. **Prioritaskan Produk yang Konsisten di Top 10:**
   Produk yang muncul di daftar top 10 untuk 30, 15, dan 7 hari terakhir menunjukkan bahwa produk ini memiliki daya tarik yang tinggi dan konsisten. Fokuskan upaya pemasaran dan promosi pada produk-produk ini.

2. **Strategi Pemasaran Berdasarkan Interaksi:**
   Produk dengan total interaksi tinggi (komentar, likes, dan views) menunjukkan minat yang tinggi dari pelanggan. Buatlah kampanye pemasaran yang memanfaatkan interaksi ini, misalnya dengan mengadakan kontes atau event yang melibatkan komentar dan likes.

3. **Tingkat Persaingan:**
   Pertimbangkan tingkat persaingan untuk setiap produk. Produk dengan banyak promotor mungkin membutuhkan strategi pemasaran yang lebih agresif atau unik untuk menonjol di antara kompetitor.

4. **Analisis Tren:**
   Lakukan analisis tren untuk melihat apakah interaksi dengan produk meningkat atau menurun. Produk dengan tren interaksi meningkat layak mendapatkan investasi lebih dalam kampanye iklan.
"""
st.markdown(rekomendasi)

# Debugging: Tampilkan informasi tambahan untuk memastikan semuanya

# Mengambil produk yang muncul di semua daftar
produk_common = set(top_products_30_days['Nama Produk']).union(set(top_products_15_days['Nama Produk']), set(top_products_7_days['Nama Produk']))

# Mengambil detail interaksi untuk produk-produk tersebut
common_products_df = df[df['Nama Produk'].isin(produk_common)]

# Menghitung total interaksi untuk setiap produk
product_stats = common_products_df.groupby('Nama Produk').agg({
    'Jumlah Komentar': 'sum',
    'Jumlah Like': 'sum',
    'Jumlah View': 'sum'
}).reset_index()

product_stats['Total Interaksi'] = product_stats['Jumlah Komentar'] + product_stats['Jumlah Like'] + product_stats['Jumlah View']

# Menghitung jumlah promotor untuk setiap produk
competition_stats = common_products_df.groupby('Nama Produk').agg({
    'User Name': 'nunique'
}).reset_index().rename(columns={'User Name': 'Jumlah Promotor'})

# Menggabungkan data interaksi dan persaingan
final_stats = pd.merge(product_stats, competition_stats, on='Nama Produk')

# Memprioritaskan produk berdasarkan total interaksi dan jumlah promotor
final_stats = final_stats.sort_values(by=['Total Interaksi', 'Jumlah Promotor'], ascending=[False, True])

# Menampilkan 10 produk teratas yang direkomendasikan
top_recommended_products = final_stats.head(10)
st.write(top_recommended_products)
