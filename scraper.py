import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import platform


def download_qs(url):

    def get_path(driver_name):
        if platform.system() == "Windows":
            return f'{os.getcwd()}/{driver_name}.exe'
        elif platform.system() == "Linux":
            return f'{os.getcwd()}/{driver_name}'

    def load_webdriver():
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
        return driver

    def download_image(image_url, image_filename):
        print(image_url)
        imagefile = requests.get(image_url).content
        print("saving file")

        with open(image_filename, mode='wb') as file:
            file.write(imagefile)

    def get_image_url(css_selector):
        image_element = driver.find_element(By.CSS_SELECTOR, css_selector)
        image_url = image_element.get_attribute("src")
        return image_url

    def download_page():
        questions = driver.find_elements(By.CSS_SELECTOR,
                                         "div.sc-iFoMEM.jzBULz")

        #questions = driver.find_elements(By.TAG_NAME, "div")
        print("questions")

        # get image and answer from first question (preselected)
        image_url = get_image_url("img.sc-jsTgWu.iWQSTV")
        filename = DOWNLOAD_PATH + image_url.split("/")[
            len(image_url.split("/")) - 1]

        download_image(image_url, filename)
        driver.find_element(By.CSS_SELECTOR, "div.sc-dkKxlM.bXWxeN").click()
        image_url = get_image_url("img.sc-jsTgWu.iWQSTV")

        download_image(image_url, filename[0:len(filename) - 4] + "_ans.png")

        for question in questions:
            print("clicking question")
            print(question.get_attribute("class"))

            question.click()

            image_url = get_image_url("img.sc-jsTgWu.iWQSTV")
            filename = DOWNLOAD_PATH + image_url.split("/")[
                len(image_url.split("/")) - 1]

            download_image(image_url, filename)

            # click on answer button and download answer file
            print("clicking answer button")
            driver.find_element(By.CSS_SELECTOR,
                                "div.sc-dkKxlM.bXWxeN").click()
            image_url = get_image_url("img.sc-jsTgWu.iWQSTV")

            download_image(image_url,
                           filename[0:len(filename) - 4] + "_ans.png")


    driver = load_webdriver()
    driver.get(url)
    print("wating for page to load")
    time.sleep(5)
    print("loaded page")

    sections = driver.find_elements(By.CSS_SELECTOR, "div.sc-kiPvrU.dSfZgv")

    download_page()

    for section in sections:
        print("section")
        section.click()
        time.sleep(0.5)

        download_page()


# Configuration options below

# URL of the page to scrape. Example of what the page should look like is provided as "example.png" .
URL = '''https://markhint.in/topical/igcse/0607/results?papers=&topics=&years=&sessions=&variants=&levels=&units=&difficulty=&page=0'''

# if its in a folder, the folder must exist (you must have created the folder) before starting downloads.
DOWNLOAD_PATH = "files/"

# set to False if difficulties are encountered. According to my testing, it will work
# with both True and False with Firefox, but only False with Chrome.
HEADLESS = True

# set to "Chrome" or "Firefox" (not case sensitive). Firefox is recommended
WEBDRIVER = "Firefox"


def main():
    download_qs(URL)


if __name__ == "__main__":
    print("start")
    main()  # To stop the script midway, press Ctrl+C
