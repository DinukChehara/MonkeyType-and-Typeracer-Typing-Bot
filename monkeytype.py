import keyboard
import json
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pyautogui
import threading

def read_words(driver):
    try:
        # finds all elements with css selector .word exlucuding ones with .word.typed
        elements = driver.find_elements(By.CSS_SELECTOR, ".word:not(.typed)") 

        words = [word.text + " " for word in elements] 
        return words
    except Exception as e:
        return False

def read_active_word(driver):
    try:
        # fins an element with css selector .word.active
        content = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".word.active"))
        )
        
        return content.text
    except Exception as e:
        return False

def type_words(driver, interval):
    while True:
            words = read_words(driver)
            if words:
                # type the words
                pyautogui.typewrite("".join(words), interval=interval)
            else:
                break
                

def type_words_with_quit_key(driver, interval):
    # initializes a thread Event/flag
    stop_flag = threading.Event()
    def type():
        while True:
            words = read_words(driver)
            if words:
                for word in words:
                    # stops the loop if the flag is set(to True)
                    if stop_flag.is_set():
                        break
                    # else continue typing each word
                    pyautogui.typewrite(word, interval=interval)
            if stop_flag.is_set():
                break

    def listen_for_stop():
        keyboard.wait("esc")
        # sets the stop_flag to True once 'esc' is pressed
        stop_flag.set()
    
    type_thread = threading.Thread(target=type, daemon=True)
    listen_thread = threading.Thread(target=listen_for_stop, daemon=True)

    type_thread.start()
    listen_thread.start()

    type_thread.join()

    return not stop_flag.is_set()

def type_active_word(driver, interval):
    while True:
        word = read_active_word(driver)
        if word:
            pyautogui.typewrite(word + " ", interval=interval)
        else:
            break

def start_up():
    with open("monkeytype_settings.json", "r") as f:
        settings = json.load(f)

    browser = settings.get("browser", "firefox").lower()
    firefox_profile_dir = settings.get("firefox_profile_dir", None)
    chrome_user_data_dir = settings.get("chrome_user_data_dir", None)
    chrome_profile_dir = settings.get("chrome_profile_dir", None)
    start_key = settings.get("start_key", "ctrl+alt+k")
    start_delay = settings.get("start_delay", 5000)
    interval = settings.get("interval", 0.25)

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if chrome_user_data_dir != None:
            options.add_argument(f"user-data-dir={chrome_user_data_dir}")
        if chrome_profile_dir != None:
            options.add_argument(f"profile-directory={chrome_profile_dir}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")  # Critical!
        options.add_argument("--disable-software-rasterizer")
        driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        driver = webdriver.Edge(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if firefox_profile_dir != None:
            options.profile = firefox_profile_dir
        driver = webdriver.Firefox(options=options)

    else:
        print("Invalid browser. Change 'browser' to chrome, firefox or edge")
        exit()

    driver.get("https://monkeytype.com")

    return {"driver": driver, "browser": browser, "chrome_user_data_dir": chrome_user_data_dir, "chrome_profile_dir": chrome_profile_dir, "firefox_profile_dir": firefox_profile_dir, "start_key": start_key, "start_delay": start_delay, "interval": interval}

def main():
    print("Openning browser...")

    data = start_up()
    start_key = data.get("start_key")
    start_delay = data.get("start_delay")
    driver = data.get("driver")
    interval = data.get("interval")

    while True:
        print("Typing bot started.\nPress '" + start_key + "' to start")

        keyboard.wait(start_key)

        print("Starting in",start_delay/1000,"seconds")

        time.sleep(start_delay/1000)

        print("Searching for words")
        # print("Press 'esc' to stop typing")
        # completed = type_words_with_quit_key(driver)
        # if not completed:
        #     print("Stopped typing")
        type_words(driver, interval=interval)
        
        cont = input("Wanna go another round? (y/n)")
        while cont.lower() not in ["y","n"]:
            cont = input("Wanna go another round? (y/n)")
        if cont == "y":
            continue
        else:
            break

if __name__ == "__main__":
    main()