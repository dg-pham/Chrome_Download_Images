import io
import time

import requests
from PIL import Image
from environ import environ
from selenium import webdriver
from selenium.webdriver.common.by import By

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

PATH = env('ENV_PATH')

# url = 'https://cdn.tgdd.vn//GameApp/-1//Screenshot(536)-800x450.png'

driver = webdriver.Chrome(PATH)


def get_images_from_google(driver, delay, max_images):
    def scroll_down(driver):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(delay)

    url = env('URL')
    driver.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(driver)

        thumbnails = driver.find_elements(By.CLASS_NAME, env('CLASS1'))

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = driver.find_elements(By.CLASS_NAME, env('CLASS2'))
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f'Found {len(image_urls)}')

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, 'wb') as f:
            image.save(f, 'PNG')

        print('Success')
    except Exception as e:
        print('FAILED -', e)


urls = get_images_from_google(driver, 1, 5)

for i, url in enumerate(urls):
    download_image('imgs/', url, str(i) + '.png')

driver.quit()
