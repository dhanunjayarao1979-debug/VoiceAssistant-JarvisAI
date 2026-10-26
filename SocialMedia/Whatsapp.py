import os
from time import sleep
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Body.Speak import Speak
from Body.Listen import MicExecution


from Config import ROOT, db_path

ListWeb = {'name_1' : "+91XXXXXXXXXX",
      'name_2': "+91XXXXXXXXXX",
      'name_3': '+91XXXXXXXXXX',
      'name_4': '+91XXXXXXXXXX',
      'name_5': '+91XXXXXXXXXX'}

driver = None


def _get_driver():
    """Start Chrome the first time WhatsApp is needed, not when this module is imported."""
    global driver
    if driver is None:
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--profile-directory=Default")
        options.add_argument(f"user-data-dir={os.path.join(ROOT, 'userdata')}")
        os.environ["WDM_LOG_LEVEL"] = "0"
        # The bundled chromedriver.exe is Windows-only; on other systems use a
        # chromedriver that matches your Chrome and is on PATH.
        driver_name = "chromedriver.exe" if os.name == "nt" else "chromedriver"
        path_of_driver = db_path(driver_name)
        if not os.path.exists(path_of_driver):
            path_of_driver = driver_name
        driver = webdriver.Chrome(path_of_driver, options=options)
        driver.maximize_window()
        driver.get("https://web.whatsapp.com/")
        Speak("Initializing Software.")
    return driver


def WhatsappSender(Name):
    driver = _get_driver()
    Speak(f"Preparing To Send a Message To {Name}")
    Speak("What's The Message By The Way?")
    Message = MicExecution()
    Number = ListWeb[Name]
    LinkWeb = 'https://web.whatsapp.com/send?phone=' + Number + "&text=" + quote(Message)
    driver.get(LinkWeb)
    sleep(5)
    try:
        driver.find_element(by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
        Speak("Message Sent")
        return True
        
        
    except:
        print("Invalid Number")
        return True

