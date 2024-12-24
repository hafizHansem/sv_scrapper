import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from  time import sleep
import csv
import json

# Membaca konfigurasi dari file JSON
with open('capabilities.json', 'r') as f:
    capabilities = json.load(f)

capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

appium_server_url = 'http://localhost:4723/wd/hub'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def swipe_up(self):
        # Mendapatkan ukuran layar
        size = self.driver.get_window_size()
        start_x = size['width'] / 2
        start_y = size['height'] * 0.8
        end_x = size['width'] / 2
        end_y = size['height'] * 0.2

        # Melakukan swipe up
        self.driver.swipe(start_x, start_y, end_x, end_y, 300)

    def get_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def get_elements(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((by, value)))

    def test_open_shopee_app(self) -> None:
        try:
            shopee_icon = self.get_element(AppiumBy.XPATH, '//*[@content-desc="Shopee" or @text="Shopee"]')
            shopee_icon.click()
            print("Shopee app opened successfully")

            video_tab_button = self.get_element(AppiumBy.XPATH, '//*[@content-desc="tab_bar_button_video"]')
            video_tab_button.click()
            print("Video tab button clicked successfully")

            while True:
                # Menunggu elemen produk muncul
                sleep(10)
                product_elements = self.get_elements(AppiumBy.XPATH, '//*[@resource-id="product tip panel"]')
                print(f"Found {len(product_elements)} product elements")

                product_name = None
                product_price = None
                like_count = None
                comment_count = None
                comment_date = None

                # Extracting product name and price
                for element in product_elements:
                    if product_name and product_price:
                        break
                    viewgroups = element.find_elements(by=AppiumBy.CLASS_NAME, value='android.view.ViewGroup')
                    for viewgroup in viewgroups:
                        if product_name and product_price:
                            break
                        text_elements = viewgroup.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
                        for text_element in text_elements:
                            text = text_element.text
                            if 'Rp' in text and not product_price:
                                product_price = text
                            elif text and not product_name:
                                product_name = text
                            if product_name and product_price:
                                break

                # Extracting like count
                like_elements = self.get_elements(AppiumBy.XPATH, '//android.view.ViewGroup[contains(@content-desc, "like")]')
                for like_element in like_elements:
                    text_elements = like_element.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
                    for text_element in text_elements:
                        text = text_element.text
                        if text:
                            like_count = text
                            break
                    if like_count:
                        break

                # Extracting comment count
                comment_elements = self.get_elements(AppiumBy.XPATH, '//android.view.ViewGroup[contains(@content-desc, "click video comment_icon")]')
                for comment_element in comment_elements:
                    text_elements = comment_element.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
                    for text_element in text_elements:
                        text = text_element.text
                        if text:
                            comment_count = text
                            break
                    if comment_count:
                        break

                # Clicking comment button
                comment_button = self.get_element(AppiumBy.XPATH, '//*[@content-desc="click video comment_icon"]')
                comment_button.click()
                print("Comment button clicked successfully")

                # Extracting comment date
                while not comment_date:
                    self.swipe_up()
                    try:
                        scroll_view = self.get_element(AppiumBy.XPATH, '//android.widget.ScrollView')
                        view_groups = scroll_view.find_elements(by=AppiumBy.CLASS_NAME, value='android.view.ViewGroup')
                        for group in view_groups:
                            group_texts = [text_element.text for text_element in group.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')]
                            if "Kreator" in group_texts:
                                for text in group_texts:
                                    if any(keyword in text for keyword in ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Oct", "Nov", "Des", "jam", "hr"]):
                                        comment_date = text
                                        break
                                if comment_date:
                                    break
                    except:
                        continue

                close_comment_panel = self.get_element(AppiumBy.XPATH, '//android.widget.ImageView[@bounds="[660,412][696,448]"]')
                close_comment_panel.click()
                print("Comment panel closed successfully")

                # Menyimpan data produk ke dalam file CSV tanpa menimpa data yang ada
                with open('product_data.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:  # Jika file kosong, tulis header
                        writer.writerow(["Product Name", "Price", "Like Count", "Comment Count", "Comment Date"])
                    writer.writerow([product_name, product_price, like_count, comment_count, comment_date])
                print("Product data saved to CSV file successfully")

                # Scroll down for next iteration
                self.swipe_up()

        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == '__main__':
    unittest.main()
