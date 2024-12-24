import os
import time
import requests

# URL yang akan digunakan untuk memeriksa koneksi internet
test_url = "http://www.google.com"

# Ganti path ke lokasi skrip sv_scrapp.py Anda yang sebenarnya
sv_scrapp_path = 'sv_scrapp.py'

# Fungsi untuk memeriksa koneksi internet
def check_internet_connection():
    try:
        # Coba mengakses test_url
        response = requests.get(test_url, timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Fungsi untuk menjalankan skrip sv_scrapp.py
def run_svScrapp():
    os.system(f'python {sv_scrapp_path}')

if __name__ == "__main__":
    while True:
        if check_internet_connection():
            print("Terhubung dengan internet. Menjalankan skrip...")
            run_svScrapp()
        else:
            print("Tidak terhubung dengan internet. Menunggu...")
        
        # Tunggu 2 menit sebelum menjalankan skrip lagi
        time.sleep(120)
