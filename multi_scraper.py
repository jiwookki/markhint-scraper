import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import platform
import threading


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

    def download_image(image_url, image_filename):
        
        imagefile = requests.get(image_url).content

        with open(image_filename, mode='wb') as file:
            file.write(imagefile)
        print(image_filename)

    def get_image_url(driver, css_selector):
        image_element = driver.find_element(By.CSS_SELECTOR, css_selector)
        image_url = image_element.get_attribute("src")
        return image_url
    


    def download_page_sequence(link_list, ndriver=None):
        if not ndriver:
            ndriver = load_webdriver()
        
        for link in link_list:
            download_page(link, ndriver=ndriver)
        
        ndriver.quit()

    def download_page(page_link, ndriver=None):

        if not ndriver:
            ndriver = load_webdriver()
        
        ndriver.get(page_link)
        time.sleep(2)

        print(f"downloading from {page_link}")


        questions = ndriver.find_elements(By.CSS_SELECTOR,
                                         "div.sc-iFoMEM.jzBULz")

        #questions = driver.find_elements(By.TAG_NAME, "div")
        print(f"{str(len(questions) + 1)} questions found in section")

        # get image and answer from first question (preselected)
        time.sleep(1)
        image_url = get_image_url(ndriver, "img.sc-jsTgWu.iWQSTV")
        filename = DOWNLOAD_PATH + image_url.split("/")[
            len(image_url.split("/")) - 1]

        download_image(image_url, filename)
        ndriver.find_element(By.CSS_SELECTOR, "div.sc-dkKxlM.bXWxeN").click()


        image_url = get_image_url(ndriver, "img.sc-jsTgWu.iWQSTV")

        download_image(image_url, filename[0:len(filename) - 4] + "_ans.png")

        for question in questions:
            #print("clicking question")
            #print(question.get_attribute("class"))

            question.click()

            image_url = get_image_url(ndriver, "img.sc-jsTgWu.iWQSTV")
            filename = DOWNLOAD_PATH + image_url.split("/")[
                len(image_url.split("/")) - 1]

            download_image(image_url, filename)

            # click on answer button and download answer file
            #print("clicking answer button")
            ndriver.find_element(By.CSS_SELECTOR,
                                "div.sc-dkKxlM.bXWxeN").click()
            image_url = get_image_url(ndriver, "img.sc-jsTgWu.iWQSTV")

            download_image(image_url,
                           filename[0:len(filename) - 4] + "_ans.png")
            
            time.sleep(0.1)
        print(f"done for {page_link}")

    

        
    section_threads = []

    driver = load_webdriver()
    driver.get(url)
    print("wating for page to load")
    time.sleep(3)
    print("loaded page")

    sections = driver.find_elements(By.CSS_SELECTOR, "div.sc-kiPvrU.dSfZgv")

    section_threads.append(threading.Thread(target=download_page, args=[driver.current_url]))

    section_urls = []

    print(f"{str(len(sections))} in page")
    time.sleep(3)

    # for section in sections:
    #     print("\nsection\n")
    #     section.click()

    #     section_urls.append(driver.current_url)

    for section in range(1, len(sections) + 1):
        # print(URL[:-1] + str(section))
        section_urls.append(URL[:-1] + str(section))

    

    prev_index = 0

    slice_size = len(section_urls)//WEBDRIVER_THREADS

    print(f"{str(slice_size)} pages per thread")


    for x in range(0, WEBDRIVER_THREADS):
        th = threading.Thread(target=download_page_sequence, args=([section_urls[prev_index:prev_index + slice_size]]))
        
        section_threads.append(th)
        prev_index += slice_size
    
    
    th = threading.Thread(target=download_page_sequence, args=([section_urls[prev_index:len(section_urls)]]))
    section_threads.append(th)

    for th in section_threads:
        th.start()
    
    for th in section_threads:
        th.join()
    
    print("downloaded all files")



# Configuration options below

# URL of the page to scrape. Example of what the page should look like is provided as "example.png" .
URL = '''https://markhint.in/topical/igcse/0610/results?papers=4%20(Extended);6&topics=&years=&sessions=&variants=&levels=&units=&difficulty=&page=0'''

# if its in a folder, the folder must exist (you must have created the folder) before starting downloads.
DOWNLOAD_PATH = "files/"

# set to False if difficulties are encountered. According to my testing, it will work
# with both True and False with Firefox, but only False with Chrome.
HEADLESS = True

# set to "Chrome" or "Firefox" (not case sensitive). Firefox is recommended
WEBDRIVER = "Firefox"

# amount of web instances that can be run at one time, for multithreading purpose. If set to one, will run as if single threaded.
WEBDRIVER_THREADS = 10


def main():
    download_qs(URL)


if __name__ == "__main__":
    print("start")
    main()  # To stop the script midway, press Ctrl+C
