import keyboard
import json
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.wpewebkit.options import Options
import pyautogui
from bs4 import BeautifulSoup
import requests

driver = webdriver.Firefox()
driver.get("https://play.typeracer.com/?rt=us9tw1k5c")

words = []

while len(words)==0:
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    words = soup.find_all(name="span", attrs={"unselectable": "on"})

words = words[0].text + words[1].text + words[2].text if len(words) == 3 else words[0].text + words[1].text
print(words)

keyboard.wait("alt+ctrl+k")

time.sleep(1)

pyautogui.typewrite(words, interval=0.07)
