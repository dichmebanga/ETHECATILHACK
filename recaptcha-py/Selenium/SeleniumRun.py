from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
import requests
import os
import whisper
import warnings

warnings.filterwarnings("ignore")
model = whisper.load_model("base")
url = "https://www.google.com/recaptcha/api2/demo"


def transcribe(url):
    try:
        with open('.temp', 'wb') as f:
            f.write(requests.get(url).content)
        result = model.transcribe('.temp')
        return result["text"].strip()
    except Exception as e:
        print(f"Lỗi trong quá trình chuyển đổi: {e}")
        return ""
    finally:
        # Xóa file tạm thời
        if os.path.exists('.temp'):
            os.remove('.temp')
            print(f"File tạm thời đã được xóa.")


def click_checkbox(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(
        By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    driver.switch_to.default_content()


def request_audio_version(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(
        By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.ID, "recaptcha-audio-button").click()


def solve_audio_captcha(driver):
    text = transcribe(driver.find_element(
        By.ID, "audio-source").get_attribute('src'))
    print('captcha', text)
    driver.find_element(By.ID, "audio-response").send_keys(text)
    driver.find_element(By.ID, "recaptcha-verify-button").click()


if __name__ == "__main__":
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    click_checkbox(driver)
    time.sleep(0.5)
    request_audio_version(driver)
    time.sleep(0.5)
    solve_audio_captcha(driver)
    # time.sleep(0.5)
    # driver.find_element(By.ID, "#recaptcha-demo-submit").click()
    time.sleep(0.5)
    driver.close()
