import requests
import pandas as pd
import json
from datetime import datetime
import os
import re

url = f'https://sv.shopee.co.id/api/v2/timeline/friends?limit=20&device_id=V9Qll8LdhYlN1LZkz%2FJ2hHe0z5lxNSO1AGwr08aQUEM%3D&is_preload=true&launch_type=1&os_type=2&system_version=24&sdk_version=1.51.3&model=Xiaomi%20Redmi%20Note%209&android_performance=187'

# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'language': 'id',
#     'did': 'V9Qll8LdhYlN1LZkz/J2hHe0z5lxNSO1AGwr08aQUEM=',
#     'fid': '70cf227bc16d8581_unknown',
#     'x-requested-from': 'rn',
#     'os-type': '2',
#     'os-system-version': '24',
#     'model': 'Xiaomi Redmi Note 9',
#     'sdk-version': '1.51.3',
#     'android-performance': '187',
#     'referer': 'trending_page',
#     'sv-from-source': 'video_tab',
#     'sv-req-timestamp': '1717653798193',
#     'sv-source-page': '',
#     'sv-pre-page': '',
#     'requestinfo': str({"deviceInfo":{"brand":"unknown","appDeviceName":"Brand/xiaomi Model/redmi_note_9 OSVer/24 Manufacturer/unknown","model":"Redmi Note 9","appOSVersion":"24","platform":0},"networkInfo":{"networkType":"wifi"},"locationInfo":{"addresses":[],"gps":{}}}),
#     'requestinfo-enc': str("%7B%22deviceInfo%22%3A%7B%22brand%22%3A%22unknown%22%2C%22appDeviceName%22%3A%22Brand%2Fxiaomi%20Model%2Fredmi_note_9%20OSVer%2F24%20Manufacturer%2Funknown%22%2C%22model%22%3A%22Redmi%20Note%209%22%2C%22appOSVersion%22%3A%2224%22%2C%22platform%22%3A0%7D%2C%22networkInfo%22%3A%7B%22networkType%22%3A%22wifi%22%7D%2C%22locationInfo%22%3A%7B%22addresses%22%3A%5B%5D%2C%22gps%22%3A%7B%7D%7D%7D"),
#     'x-request-id': '000003eb1a32707d0f3f000000000000:0000000000000000:0000000000000000',
#     'sfid': 'oMSrG6guhvM6fNyrCA/i+g==|hwpx6JLEKdXrvc1RG0ZO9gUh8hsqZkxgalz8E5cYxWJWIl3svJY6HzfL6cjrQIGSOn+s1iNFODn9ucT3Lp+CNyAyalqOYA==|D8OBONonAxaSSzZ6|08|1',
#     'x-shopee-client-timezone': 'America/New_York',
#     'client-request-id': 'b8178bcf-f1fc-4002-b66d-0f267a96b65a.84',
#     'content-type': 'application/json',
#     'content-length':"301",
#     'cookie': 'userid=0; shopid=0; username=null; shopee_token=null; language=id; shopee_app_version=32709; SPC_CLIENTID=V9Qll8LdhYlN1LZkrqxizahpvpgymvxd; SPC_AFTID=3a4e0ba3-45e8-460a-b8a2-683483102b66; shopee_rn_version=1716550498; SPC_F=70cf227bc16d8581_unknown; UA=Shopee%20Android%20Beeshop%20locale%2Fid%20version%3D32709%20appver%3D32709; csrftoken=AEHfdDy045zRtaceVH8O8Ckp8WB0xzyL',
#     'user-agent': 'okhttp/3.12.4 app_type=1',
#     'af-ac-enc-dat': 'YWNzCjAwNAAQgYhxG6Yi7I8BAAABAQEAEAEAAEQm2D18ngXU8ZiC0BaVWP/OqykE6bN6xjBPsyF7lrj41WJ2Z7WgLmr7tzkhowh8pxThyh2/Jo5sfoVyCOWgliDu4pQgOQ1EPFVwWlQUYsAhkyvRRScIe1W845bMD94N9gjFBFvBxBCRjh0rVP0UNSlS2N5BA2qY/T/dT8MeiL6pUhQhHhDhRgU6nhfu9gZBww+KQvPj0JVQGUY/NH76YgTLEDeawav9Mq3Y+E7IAdeiCPxqOZBBHif8pj4l2GzMrSt9b10a13xWKHJxHrPxYl9Z2/xVmwP0wcTfcxJyGWCUQ5Y9SbdUn85Q6DoepyhL5muEOjt4iPyCc6V03FSLvN/tLo4TktaJEQ00kRps+OKN',
#     'af-ac-enc-id': '6FPmlQA2iPLrm+OqxxY8Wp2YBwVqEgR0b27U7A4pv6fADjaTecRCHFyCoKH/YuGmUFLYTA==',
#     'af-ac-enc-sz-token': 'oMSrG6guhvM6fNyrCA/i+g==|hwpx6JLEKdXrvc1RG0ZO9gUh8hsqZkxgalz8E5cYxWJWIl3svJY6HzfL6cjrQIGSOn+s1iNFODn9ucT3Lp+CNyAyalqOYA==|D8OBONonAxaSSzZ6|08|1',
#     'b5996a06': '4f5xX/zufAWbcFJBb9JLdda3hGMfOBnbZjk2CzhFKL5l2P8D22WfdWHXRaXgrD5htlbrNQzanBO+REacKgn+jJwxBrn20qeGLSWr3fsLinmmv8ynt8fCYc9l16aRfaQJQLPRTKY8wCqWSOTQPq9WYmAPdxiojz6W/XMiIFX0WwWrulINq2YmzLKdBd/v7XjBCGQOfjak1UK0SMXI3ASEQ1vx6tFNLU1d3hTz5e4fyQbuLhWeBAMApWx9jJP6utU1z5Ao1YW2wZvGVT5B1MdNuGvEbmCwUgjrXU99JS3/nUAMnULDaOUQ68eY1mZaHeQT7VJcfb6Kk6DCBngeZ0Yvnca/mjUXmPrNjDTvRWdqAdcfRCGvRftlqhqQgauaO92alJHmLkQkCAQNdLKumzoPjRXrvbyLm0m1Wuy4jNJl2iIyrNomMjX8DcJ1jhqJghSx75DZypH8C6I8MAnl9e6qLbxhbPkJ9qLGrIm6cjBQo7oInV8AZz5Py/kWEeAAhMCZvNjVShk5ar3OeYF2aB5fjbvWr/2fsbdSOmkBRo0zYTPOPul/T4q3vlr4+Z36jFxCUWTAXP6F6RQ9tBoJPEra995yhjLOFAVvcUdOsTRpgnL6Rji6unDtj8nNuUt0TVs1wbJxnaGgGU6MX12EU9L56gwOCVUzHfhz/N7awIcjBHxPbd+e+e8GNikoNWFoKcdRoJXQsGOsSYNmqx/rYAdzWqGoSzzZq4ZFrOBy9HclNKBsyZyXg64qMNJBoHWUGs1TV8hOHQrazmq0C5Fq',
#     '4619323a':'jr1iMyKAdoVZrfGE2b1tPNJ5uFy=',
#     'x-sap-ri': '2651616665df263d58cbdb190169bd1944b024813dde727e0242',
#     '23bc3170': 'gi0yilroNEGWfZX80tyxcjzyNyt=',
#     '4715a708': 'LTf6oiR52A2gYzhJ73l7fOgv5YT=',
#     'x-csrftoken': 'AEHfdDy045zRtaceVH8O8Ckp8WB0xzyL',
# }


headers = {
    "sv-from-source": "hot_start",
    "fid": "70cf227bc16d8581_unknown",
    "client-info": f"device_id=V9Qll8LdhYlN1LZkz%2FJ2hHe0z5lxNSO1AGwr08aQUEM%3D;device_model=Redmi+Note+9;os=0;os_version=24;client_version=32709;network=1;platform=1;rn_version=6.18.5;api_source=na",
    "language": "id",
    "referer": "HomeActivity_",
    "sfid": "oMSrG6guhvM6fNyrCA/i+g==|hwpx6JLEKdXrvc1RG0ZO9gUh8hsqZkxgalz8E5cYxWJWIl3svJY6HzfL6cjrQIGSOn+s1iNFODn9ucT3Lp+CNyAyalqOYA==|D8OBONonAxaSSzZ6|08|1",
    "x-shopee-client-timezone": "America/New_York",
    "client-request-id": "50665c8e-ba28-4648-8ddc-2db370aa2ccc.64",
    "accept-encoding": "gzip",
    "cookie": "userid=0; shopid=0; username=null; shopee_token=null; language=id; shopee_app_version=32709; SPC_CLIENTID=V9Qll8LdhYlN1LZkrqxizahpvpgymvxd; SPC_AFTID=3a4e0ba3-45e8-460a-b8a2-683483102b66; shopee_rn_version=1716550498; SPC_F=70cf227bc16d8581_unknown; UA=Shopee%20Android%20Beeshop%20locale%2Fid%20version%3D32709%20appver%3D32709; csrftoken=fCrq9SiLh7V1KtOkbFOBzWCiy9HsHkLl",
    "if-modified-since": "Thu, 06 Jun 2024 06:02:30 GMT",
    "user-agent": "okhttp/3.12.4 app_type=1",
    "af-ac-enc-dat": "YWNzCjAwNADtiEiKGR2FYpABAAABAQEAEAEAAEQm2D18ngXU8ZiC0BaVWP/E9hVOn1nA3GldlbrzNPQe+a2ZbLY5IDyyJGGlXJHFBQXNgZZhl9R0056vgesQYFanGj2f71BanRdEKu77HH/EYV++QRNZmLHfFKiXljQHhhnmKvDWaLzTM+ckY1z6jmL0Z6oIXJ4yEiOrEqDOb/BvOiEpsPtZ0UoWr8Lf0imsTT0jZPofg+f4ltKRMpdVBOCpD/r9z1xfZmFagfllI8e8g0UTt5P4svNwpplq/x/FRj3W3adhgNVqB5frEojoWT9YBgcWcdNKbeja4HYx4G/tENWnSWEdiyfkKV9nUoIjn8DjIbO0ZijjGhS4l0K+e0aKIZN13Adaer7Gw479ZT8y",
    "af-ac-enc-id": "Kpba7CQmXJsRBLAn+9ChcSFdpVG2zV/SrE7pXn8irJCHH4ftsfup1u6gN7ca9wG2V3DMaA==",
    "af-ac-enc-sz-token": "1DXQRnDvg8OySMqCMjSevA==|gApx6JLEKdXrvc1RG0ZO9gUh8hsqZkxgalz8E81KY+xJIl3svJT2VTsJursMJs2ryN0LOw9FODn9ucT3Lp+CNSAyalqOYA==|D8OBONonAxaSSzZ6|08|1",
    "d8feda18": "RAjgxEGBQjxkuYTDqm77Rl8V9l9b5kdks6XuL5RxNGg3gqwOh74KhCZYI8NHII/2fAB1i65p701oPJtaNiZRCxWI3dYq2YLtQJailGD7ofcJKdmtS8yB5HdXf/HR39wMzKlv+mo8pI1bvet4zToVFYz/BJBKBFJwUVw7lXaXtdwtR/wb3dh08kS7qz8HezzJWocv1iVi2BK7kEFashr6MBNutkaivqFlC8uHHniEW68LSs349SBVRYmS/Mspx69CZdpUNphO/tNLmPEYHGWEFSJAyJ117l1vho8vek1CfWxq79zSFHqF2BCNblYp3NA1unRo+PDx+YveFa4lXcyMsIrWwSCZ2Vxe6Vq6St1MEWlDDPw3MiAUvaJJIn8DgXOB+yydO/obWDU78NI0dCxGoxXe7+aYP3Jfzi+PLvWzywkOG9ewufhs30oF2h3K9hB7lSUWpfRX8Xdg4B6maRxy128l3D85VLQ8Vzxyy++iQ3I7zuGa7KSKR5xitLwalsGReITd0hbZ7uKs8zxdu1TXZxdhDvq6uOupQDBL9bS0vzUAb+OwRrvmEbPzWjqGKwDsTLH4oW7ZZ4KGHcwnXbIqRgcG3cZdu1hyQNJtxq2rkjzRFdmmZZ2c02xhIILdyyqXv9bx51dsCeYCDXeeKbfECdHA+3SoWg3keYtkhV44Ot4VO5bALif7Sr/nuqbImlV5ikuNo28j/wzHcPcu",
    "x-sap-ri": "aa9f7f66e898ae26cf96ec120131a210d3a5d4274c8190a2cdb8",
    "13ceb317": "ZyhfYGxxFGCMeWi346Y+rLTToXj=",
    "54e87ab6": "ZX1FdLpzoT8pfNGnXcp4ty34r8j="
}


# # Definisikan payload data yang akan dikirim dalam bentuk JSON
# payload = {
#     "limit": 6,
#     "page_context": None,
#     "device_id": "V9Qll8LdhYlN1LZkz/J2hHe0z5lxNSO1AGwr08aQUEM=",
#     "rec_request_info": {
#         "dayPages": 2,
#         "sessionPages": 2,
#         "interactDataFromVideo": [],
#         "interactDataFromCard": [],
#         "sessionCards": 0
#     },
#     "request_type": 0,
#     "ext_info": [
#         {"key": "ads_entrance", "value": "29"}
#     ],
#     "lang": "id"
# }

# Mengubah payload menjadi JSON
#json_payload = json.dumps(payload)

# Mengirim permintaan POST dengan menggunakan requests
response = requests.get(url, headers=headers)

# formatted_response = json.dumps(response.json(), indent=4)

# print(formatted_response)


# Fungsi untuk memperbaiki harga
def correct_price(price):
    return price // 100000  # Mengurangi 5 angka 0 dari belakang

# Fungsi untuk konversi timestamp
def convert_timestamp(ts):
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Fungsi untuk ekstraksi hashtag dari caption
def extract_hashtags(caption):
    return re.findall(r'#\w+', caption)

data = response.json()


# List untuk menyimpan data utama dan hashtags
main_rows = []
hashtag_rows = []

# Proses data untuk mendapatkan informasi yang dibutuhkan
# for item in data['data']['list']:
#     post = item['post']
#     meta = post['meta']
#     content = post['content']
    
#     post_id = meta['post_id']
#     user_id = meta['user_id']
#     user_name = meta['user_name']
#     comment_count = meta['count_info']['comments']
#     like_count = meta['count_info']['likes']
#     view_count = meta['count_info']['views']
#     post_date = convert_timestamp(meta['ctime'])
    
#     product_name = content['products']['anchor_product']['name']
#     offer_link = content['products']['anchor_product']['offer_link']
#     product_price = correct_price(content['products']['anchor_product']['price'])
#     caption = content.get('caption', '')

#     # Tambahkan ke dalam list main_rows
#     main_rows.append({
#         'Post ID': post_id,
#         'User ID': user_id,
#         'User Name': user_name,
#         'Nama Produk': product_name,
#         'Link Penawaran': offer_link,
#         'Jumlah Komentar': comment_count,
#         'Jumlah Like': like_count,
#         'Jumlah View': view_count,
#         'Tanggal Post': post_date,
#         'Harga Produk': product_price,
#         'Caption': caption
#     })

#     # Proses hashtags dari caption
#     hashtags = extract_hashtags(caption)
#     for hashtag in hashtags:
#         hashtag_id = f"{post_id}_{hashtag}"
        
#         hashtag_rows.append({
#             'Post ID': post_id,
#             'Timestamp': meta['ctime'],
#             'Hashtag ID': hashtag_id,
#             'Hashtag': hashtag
#         })


# data = response.json()
# List untuk menyimpan data utama dan hashtags
# main_rows = []
# hashtag_rows = []

# Proses data untuk mendapatkan informasi yang dibutuhkan
for post in data['data']['list']:
    meta = post['meta']
    content = post['content']
    
    post_id = meta.get('post_id')
    user_id = meta.get('user_id')
    user_name = meta.get('user_name')
    comment_count = meta['count_info'].get('comments', 0)
    like_count = meta['count_info'].get('likes', 0)
    view_count = meta['count_info'].get('views', 0)
    post_date = convert_timestamp(meta.get('ctime'))
    
    product_name = content['products']['anchor_product'].get('name', '')
    offer_link = content['products']['anchor_product'].get('offer_link', '')
    product_price = correct_price(content['products']['anchor_product'].get('price', 0))
    caption = content.get('caption', '')

    # Tambahkan ke dalam list main_rows
    main_rows.append({
        'Post ID': post_id,
        'User ID': user_id,
        'User Name': user_name,
        'Nama Produk': product_name,
        'Link Penawaran': offer_link,
        'Jumlah Komentar': comment_count,
        'Jumlah Like': like_count,
        'Jumlah View': view_count,
        'Tanggal Post': post_date,
        'Harga Produk': product_price,
        'Caption': caption
    })

    # Proses hashtags dari caption
    hashtags = extract_hashtags(caption)
    for hashtag in hashtags:
        hashtag_id = f"{post_id}_{hashtag}"
        
        hashtag_rows.append({
            'Post ID': post_id,
            'Timestamp': meta.get('ctime'),
            'Hashtag ID': hashtag_id,
            'Hashtag': hashtag
        })




# Buat DataFrame dari list main_rows
df_main = pd.DataFrame(main_rows)
# Buat DataFrame dari list hashtag_rows
df_hashtags = pd.DataFrame(hashtag_rows)

# Tentukan nama file CSV
main_file_name = 'scraped_sv_product_data.csv'
hashtag_file_name = 'scraped_sv_hashtags.csv'

# Simpan DataFrame utama ke file CSV
if os.path.isfile(main_file_name):
    df_main.to_csv(main_file_name, mode='a', header=False, index=False)
else:
    df_main.to_csv(main_file_name, mode='w', header=True, index=False)

# Simpan DataFrame hashtags ke file CSV
if os.path.isfile(hashtag_file_name):
    df_hashtags.to_csv(hashtag_file_name, mode='a', header=False, index=False)
else:
    df_hashtags.to_csv(hashtag_file_name, mode='w', header=True, index=False)

# Tampilkan panjang data (jumlah baris) yang baru saja di-scrap
# print("Panjang data yang baru di-scrap:", len(df_main))
# print("Panjang data hashtags yang baru di-scrap:", len(df_hashtags))

# Tampilkan DataFrame yang baru di-scrap
# print(df_main)
# print(df_hashtags)

print("Panjang data yang baru di-scrap:", len(df_main))
print("Panjang data hashtags yang baru di-scrap:", len(df_hashtags))

# df_main
