from selenium import webdriver
from selenium.webdriver.common.by import By
import os 
import platform 
import time
import multi_scraper_mcq


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
    topic_texts = []
    for topic in topics:
        topic_texts.append(topic.text)
    driver.find_element(By.ID, "get-questions-button").click()

    return topic_texts, driver.current_url
    
        

        #print(topic.find_element(By.CSS_SELECTOR, "div.sc-eGugkK.dDccTP"))



def download_all_topics_qs(topics, base_url):
    keyword = "&topics="
    for topic in topics:
        print(base_url[:base_url.find(keyword)] + topic + base_url[base_url.find(keyword)+len(keyword):])
        multi_scraper_mcq.download_qs(OUTPUT_BASE_DIRECTORY + topic + "/", base_url[:base_url.find(keyword) + len(keyword)] + topic + base_url[base_url.find(keyword) + len(keyword):])

    


#s[:s.find(xs)] + "white" + s[s.find(xs)+len(xs):]



SEARCH_LINK  = "https://markhint.in/topical"

DOWNLOAD_LINK = ""

OUTPUT_FILENAME = "topics.txt"

OUTPUT_BASE_DIRECTORY = "files/"

WEBDRIVER = "Firefox"

HEADLESS = False

TOPIC_LIST = [] 



if __name__ == "__main__":
    TOPIC_LIST, DOWNLOAD_LINK = get_topics()
    download_all_topics_qs(TOPIC_LIST, DOWNLOAD_LINK)


