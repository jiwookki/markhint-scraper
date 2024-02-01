import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import os 
import platform 
import time


def load_webdriver():
        def get_path(driver_name):
            if platform.system() == "Windows":
                return f'{os.getcwd()}/{driver_name}.exe'
            elif platform.system() == "Linux":
                return f'{os.getcwd()}/{driver_name}'
        driver = None
        if WEBDRIVER.upper() == "CHROME":
            print("WEBDRIVER: CHROME")
            execpath = get_path("chromedriver")
            print(execpath)
            service = webdriver.ChromeService(executable_path=execpath)
            options = webdriver.ChromeOptions()
            if HEADLESS:
                options.add_argument("-headless")

            driver = webdriver.Chrome(service=service, options=options)

        elif WEBDRIVER.upper() == "FIREFOX":
            print("WEBDRIVER: FIREFOX")
            execpath = get_path("geckodriver")
            print(execpath)
            service = webdriver.FirefoxService(executable_path=execpath)
            #service = webdriver.FirefoxService()
            options = webdriver.FirefoxOptions()
            if HEADLESS:
                options.add_argument("-headless")

            driver = webdriver.Firefox(service=service, options=options)
        elif WEBDRIVER.upper() == "EDGE":
            print("WEBDRIVER: EDGE")
            execpath = get_path("msedgedriver")
            print(execpath)
            service = webdriver.EdgeService(executable_path=execpath)
            #service = webdriver.FirefoxService()
            options = webdriver.EdgeOptions()
            if HEADLESS:
                options.add_argument("-headless")

            driver = webdriver.Edge(service=service, options=options)
        return driver

def get_topics():
    driver = load_webdriver()
    driver.get(SEARCH_LINK)
    print("set up the topics and stuff first")
    for x in range(1, 15):
        print(15-x)
        time.sleep(1)
    
    topic_dropdown = driver.find_element(By.ID, "topics-dropdown")
    topic_dropdown.click()
    print(topic_dropdown.find_element(By.CSS_SELECTOR, "div.sc-bWOGAC.dTkoAY"))
    topics = topic_dropdown.find_element(By.CSS_SELECTOR, "div.sc-bWOGAC.dTkoAY").find_elements(By.CSS_SELECTOR, "div.sc-dEVLtI.lYhMC")
    #topics = topic_dropdown.find_element(By.CSS_SELECTOR, "div.sc-bWOGAC.dTkoAY").find_elements(By.CSS_SELECTOR, "div.sc-eGugkK.dDccTP")
    print(len(topics))
    for topic in topics:
        print(topic.text)
        #print(topic.find_element(By.CSS_SELECTOR, "div.sc-eGugkK.dDccTP"))










SEARCH_LINK  = "https://markhint.in/topical"


OUTPUT_FILENAME = "topics.txt"

WEBDRIVER = "Firefox"

HEADLESS = False


if __name__ == "__main__":
    get_topics()
