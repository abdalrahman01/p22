from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


option = webdriver.ChromeOptions()
option.binary_location = "./chrome-linux64/chrome"
driver = webdriver.Chrome(option)
driver.get("http://127.0.0.1:7860")

while True:
    time.sleep(1)
    print(driver.title)