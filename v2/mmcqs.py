import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import platform
import threading
from pathlib import Path
from urllib import parse



def get_topic_qs_threads(download_path, url):

    global TOPIC_THREADS

    # this function is single threaded


    def create_edge_driver():
        path = "./msedgedriver.exe"
        
        service = webdriver.EdgeService(executable_path=path)

        options = webdriver.EdgeOptions()
        options.add_argument("-headless")

        driver = webdriver.Edge(options=options, service=service)
        return driver

    def create_driver():
        #path = "./geckodriver"
        path = "./geckodriver.exe"

        service = webdriver.FirefoxService(executable_path=path)




        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

        driver = webdriver.Firefox(options=options, service=service)

        return driver


    def create_safari_driver():

        #path = "safaridriver"

        #service = webdriver.SafariService(executable_path=path)
        options = webdriver.SafariOptions()
        options.add_argument("-headless")

        driver = webdriver.Safari(options=options)

        return driver



    def download_image(image_url, image_filename):
        
        imagefile = requests.get(image_url).content

        with open(image_filename, mode='wb') as file:
            file.write(imagefile)
        print(image_filename)



    def get_image_url(driver : DRIVERTYPE, css_selector):
        image_element = driver.find_element(By.CSS_SELECTOR, css_selector)
        image_url = image_element.get_attribute("src")
        return image_url
    



    def download_page_sequence(download_path, link_list, ndriver=None):
        print(f"down path: {download_path}")
        if not ndriver:
            ndriver = create_driver()
        
        for link in link_list:
            download_page(download_path, link, ndriver=ndriver)

        ndriver.close()
        ndriver.quit()



    def download_page(download_path, page_link, ndriver=None):

        #print(type(page_link))

        assert isinstance(page_link, str)

        if not ndriver:
            ndriver = create_driver()
        
        ndriver.get(page_link)
        time.sleep(2)

        print(f"downloading from {page_link}")


        questions = ndriver.find_elements(By.CSS_SELECTOR,
                                         NEXT_QUESTION_SELECTOR)

        #questions = driver.find_elements(By.TAG_NAME, "div")
        print(f"{str(len(questions) + 1)} questions found in section")

        # get image and answer from first question (preselected)
        time.sleep(1)
        image_url = get_image_url(ndriver, QUESTION_CONTENT_SELECTOR)
        filename = download_path + image_url.split("/")[
            len(image_url.split("/")) - 1]

        download_image(image_url, filename)
        ndriver.find_element(By.CSS_SELECTOR, ANSWER_SWITCH_SELECTOR).click()


        answer_element = ndriver.find_element(By.CSS_SELECTOR, ANSWER_CONTENT_SELECTOR)

        with open(filename[0:len(filename) - 4] + "_ans.txt", "w") as txtfile:
            txtfile.write(answer_element.text)
        print(filename[0:len(filename) - 4] + "_ans.txt")

        for question in questions:
            #print("clicking question")
            #print(question.get_attribute("class"))

            question.click()

            image_url = get_image_url(ndriver, QUESTION_CONTENT_SELECTOR)
            filename = download_path + image_url.split("/")[
                len(image_url.split("/")) - 1]

            download_image(image_url, filename)

            # click on answer button and download answer file
            #print("clicking answer button")
            ndriver.find_element(By.CSS_SELECTOR,
                                ANSWER_SWITCH_SELECTOR).click()
            
            

            
            answer_element = ndriver.find_element(By.CSS_SELECTOR, ANSWER_CONTENT_SELECTOR)

            with open(filename[0:len(filename) - 4] + "_ans.txt", "w") as txtfile:
                txtfile.write(answer_element.text)
            print(filename[0:len(filename) - 4] + "_ans.txt")
        
            

            


            
            time.sleep(0.1)
        print(f"done for {page_link}")

    
    # ----- MAIN ----- 
        
    section_threads = []

    driver = create_driver()
    driver.get(url)
    print("wating for page to load")
    time.sleep(3)
    print("loaded page")

    sections = driver.find_elements(By.CSS_SELECTOR, SECTONS_SELECTOR)

    section_urls = [driver.current_url]

    print(f"{str(len(sections))} in page")
    time.sleep(3)

    # for section in sections:
    #     print("\nsection\n")
    #     section.click()

    #     section_urls.append(driver.current_url)

    for section in range(1, len(sections) + 1):
        # print(URL[:-1] + str(section))
        section_urls.append(url[:-1] + str(section))


    section_urls_list = []
    for x in range(0, WEBDRIVER_THREADS):
        section_urls_list.append([])

    sxc = 0    
    
    for url in section_urls:
        section_urls_list[sxc].append(url)
        sxc+=1
        if sxc == WEBDRIVER_THREADS-1:
            sxc = 0
    
    Path(download_path).mkdir(parents=True, exist_ok=True)

    driver.quit()

    for urls in section_urls_list:
        print(urls)

    # time.sleep(5)

    for urls in section_urls_list:
        # th = threading.Thread(target=download_page_sequence, args=(download_path, url_slice))
        # section_threads.append(th)
        th = threading.Thread(target=download_page_sequence, args=(download_path, urls))
        TOPIC_THREADS.append(th)
    




def download_subject(topics):
    global TOPIC_THREADS

    baseurl = BASE.replace("[[SUBJECT]]", SUBJECT)
    baseurl = baseurl.replace("[[PAPERS]]", PAPERS)

    print(baseurl)
    time.sleep(5)

    TOPIC_THREADS = []

    tgetthreads = []

    for topic in topics:

        newurl = baseurl.replace("[[TOPICS]]", parse.quote(topic))
        # th = threading.Thread(target=get_topic_qs_threads, args=(DOWNLOAD_PATH+topic+"/", newurl))
        
        #nt = get_topic_qs_threads(DOWNLOAD_PATH+topic+"/", newurl)
        nt = threading.Thread(target=get_topic_qs_threads, args=(DOWNLOAD_PATH+topic+"/", newurl))

        tgetthreads.append(nt)

    for tgh in tgetthreads:
        tgh.start()

    for tgh in tgetthreads:
        tgh.join()


    print("start download")

    for th in TOPIC_THREADS:
        th.start()
    
    for th in TOPIC_THREADS:
        th.join()

    print("all done")

    
        


# Configuration options below


SUBJECT = "0625"

# https://markhint.in/topical/igcse/0620/results?papers=&topics=&years=&sessions=&variants=&levels=&units=&difficulty=&page=0

# BASE = "https://markhint.in/topical/igcse/[[SUBJECT]]/results?"

BASE = "https://markhint.in/topical/igcse/[[SUBJECT]]/results?papers=[[PAPERS]]&topics=[[TOPICS]]&years=&sessions=&variants=&levels=&units=&difficulty=&page=0"

# example [[PAPERS]] = 1%20(Core);2%20(Extended)

# example [[TOPICS]] = CH%201%20-%20STATES%20OF%20MATTER

# example [[SUBJECT]] = 0620

PAPERS = "2%20(Extended)"


OUTF = "topics.txt"



#https://markhint.in/topical/igcse/0620/results?papers=1%20(Core);2%20(Extended)&topics=CH%201%20-%20STATES%20OF%20MATTER&years=&sessions=&variants=&levels=&units=&difficulty=&page=0
#https://markhint.in/topical/igcse/0620/results?papers=1%20(Core);2%20(Extended)&topics=&years=&sessions=&variants=&levels=&units=&difficulty=&page=0



# if its in a folder, the folder must exist (you must have created the folder) before starting downloads.
DOWNLOAD_PATH = "files/"

# set to False if difficulties are encountered. According to my testing, it will work
# with both True and False with Firefox, but only False with Chrome.
HEADLESS = True

# set to "Chrome" or "Firefox" (not case sensitive). Firefox is recommended
WEBDRIVER = "Firefox"

DRIVERTYPE = webdriver.Safari

# amount of web instances that can be run at one time, for multithreading purpose. If set to one, will run as if single threaded.
WEBDRIVER_THREADS = 3



# --- CONFIGURATIONS FOR QUESTION/ANSWER DETECTION 

SECTONS_SELECTOR = "div.sc-eYqcxL.ZJhRy" # switch between question tabs (top row)

QUESTION_CONTENT_SELECTOR = "img.sc-gkSfol.kBYqqH" # used to identify the question itself

ANSWER_SWITCH_SELECTOR = "div.sc-elAWhN.bksjud" # clicked to switch from question to answer

ANSWER_CONTENT_SELECTOR = "div.sc-cLNonn.faNhRA" # used to identify the correct answer

NEXT_QUESTION_SELECTOR = "div.sc-hjjlnc.cxFfoP" # used to select the next question in the list



def main():
    with open("topics.txt", "r") as nf:
        topics = nf.read().split("\n")
    print(topics)
    download_subject(topics)


if __name__ == "__main__":
    print("start")
    main()  # To stop the script midway, press Ctrl+C
