
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import parse
import time




URL = '''https://markhint.in/topical'''

def create_driver():
    path = "./geckodriver.exe"

    service = webdriver.FirefoxService(executable_path=path)




    options = webdriver.FirefoxOptions()
    #options.add_argument("-headless")
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

    driver = webdriver.Firefox(options=options, service=service)

    return driver


def create_safari_driver():

    #path = "safaridriver"

    #service = webdriver.SafariService(executable_path=path)
    options = webdriver.SafariOptions()
    #options.add_argument("-headless")

    driver = webdriver.Safari(options=options)

    return driver

def get_topics(driver):

    # def select_dropdown(driver, dropdown_text, index):
    #     dropdowns = driver.find_elements(By.CSS_SELECTOR, "div.sc-cZFQFd.bokGRY")

    #     time.sleep(0.5)
    #     sdrop = None

    #     for dropdown in dropdowns:
    #         print(dropdown.text)
    #         print(dropdown)
    #         if dropdown_text in dropdown.text:
    #             dropdown.click()
    #             print("clicked")
    #             sdrop = dropdown
    #     #boarddropdown.click()

    #     time.sleep(1)
    #     #dropdowns[1].click()

    #     itemlist = driver.find_element(By.CSS_SELECTOR, "div.sc-fvEvSO.fzjNjw").find_elements(By.CSS_SELECTOR, "div.sc-gsGlKL.URrNE")
    #     for item in itemlist:
    #         print(item.text)
        
    #     itemlist[index].click()

    def _get_in_dropdowns(driver):
        return driver.find_elements(By.CSS_SELECTOR, "div.sc-cZFQFd.bokGRY")
    
    def click_dropdown(driver, dropdown_text):
        dropdowns = _get_in_dropdowns(driver)

        time.sleep(0.5)
        sdrop = None

        for dropdown in dropdowns:
            print(dropdown.text)
            print(dropdown)
            if dropdown_text in dropdown.text:
                dropdown.click()
                print("clicked")
                sdrop = dropdown
        return sdrop


    def select_dropdown(driver, dropdown_text, index):

        time.sleep(0.5)
        click_dropdown(driver, dropdown_text)
        #boarddropdown.click()

        time.sleep(1)
        #dropdowns[1].click()

        itemlist = driver.find_element(By.CSS_SELECTOR, "div.sc-fvEvSO.fzjNjw").find_elements(By.CSS_SELECTOR, "div.sc-gsGlKL.URrNE")
        for item in itemlist:
            print(item.text)
        
        itemlist[index].click()

    
    def find_select_dropdown(driver, dropdown_text, index_text):
        click_dropdown(driver, dropdown_text)
        time.sleep(1)
        #dropdowns[1].click()

        itemlist = driver.find_element(By.CSS_SELECTOR, "div.sc-fvEvSO.fzjNjw").find_elements(By.CSS_SELECTOR, "div.sc-gsGlKL.URrNE")
        for item in itemlist:
            print(item.text)
            if index_text in item.text:
                print("found")
                item.click()
                break
    
    def get_all_dropdowns(driver, dropdown_text):
        click_dropdown(driver, dropdown_text)
        #boarddropdown.click()

        time.sleep(1)
        #dropdowns[1].click()

        itemlist = driver.find_element(By.CSS_SELECTOR, "div.sc-fvEvSO.fzjNjw").find_elements(By.CSS_SELECTOR, "div.sc-gsGlKL.URrNE")
        out_list = {}
        for item in itemlist:
            out_list[item.text] = item
        
        return out_list






    driver.get(URL)

    time.sleep(3)

    boarddropdown = driver.find_element(By.CSS_SELECTOR, "div.sc-dsHJmm.ehBGBb")
    boarddropdown.click()

    time.sleep(0.5)

    boardlist = boarddropdown.find_element(By.CSS_SELECTOR, "div.sc-fvEvSO.fzjNjw").find_elements(By.CSS_SELECTOR, "div.sc-gsGlKL.URrNE")
    for board in boardlist:
        print(board.text)
    boardlist[0].click()
    time.sleep(0.5)

    print("\n\n")
    
    select_dropdown(driver, "Subject", 7)

    time.sleep(1)

    select_dropdown(driver, "Paper", 0)

    time.sleep(0.2)

    select_dropdown(driver, "Paper", 1)

    time.sleep(0.5)

    #click_dropdown(driver, "Topics")


    topics = get_all_dropdowns(driver, "Topics")

    # find_select_dropdown(driver, "Topics", topic)

    # time.sleep(0.5)

    # driver.find_element(By.ID, "get-questions-button").click()
    


    #return driver.current_url

    return topics

    




SUBJECT = "0620"
# https://markhint.in/topical/igcse/0620/results?papers=&topics=&years=&sessions=&variants=&levels=&units=&difficulty=&page=0
# BASE = "https://markhint.in/topical/igcse/[[SUBJECT]]/results?"
BASE = "https://markhint.in/topical/igcse/[[SUBJECT]]/results?papers=[[PAPERS]]&topics=[[TOPICS]]&years=&sessions=&variants=&levels=&units=&difficulty=&page=0"
# example [[PAPERS]] = 1%20(Core);2%20(Extended)
# example [[TOPICS]] = CH%201%20-%20STATES%20OF%20MATTER
# example [[topics]] = CH%201%20-%20STATES%20OF%20MATTER
# example [[SUBJECT]] = 0620

OUTF = "topics.txt"



#https://markhint.in/topical/igcse/0620/results?papers=1%20(Core);2%20(Extended)&topics=CH%201%20-%20STATES%20OF%20MATTER&years=&sessions=&variants=&levels=&units=&difficulty=&page=0
#https://markhint.in/topical/igcse/0620/results?papers=1%20(Core);2%20(Extended)&topics=&years=&sessions=&variants=&levels=&units=&difficulty=&page=0


def main():
    driver = create_driver()
    try:
        

        
        t = get_topics(driver)
        print(f"got {str(len(t))} topics")

        outp = "\n".join(t.keys())

        with open(OUTF, "w") as of:
            of.write(outp)
        
        print("done")


    except Exception as ex:
        print(f"[HEY] encountered {str(type(ex))} {str(ex)}")

    finally:
        time.sleep(8)
        driver.quit()





if __name__ == "__main__":
    main()





