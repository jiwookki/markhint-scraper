
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

import time




URL = '''https://markhint.in/topical'''

def create_firefox_driver():
    path = "./geckodriver"

    service = webdriver.FirefoxService(executable_path=path)




    options = webdriver.FirefoxOptions()
    #options.add_argument("-headless")

    driver = webdriver.Firefox(options=options, service=service)

    return driver


def create_driver():

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


    def select_dropdown(driver, dropdown_text, index):
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
        #boarddropdown.click()

        time.sleep(1)
        #dropdowns[1].click()

        itemlist = driver.find_element(By.CSS_SELECTOR, "div.sc-fvEvSO.fzjNjw").find_elements(By.CSS_SELECTOR, "div.sc-gsGlKL.URrNE")
        for item in itemlist:
            print(item.text)
        
        itemlist[index].click()

    
    def find_select_dropdown(driver, dropdown_text, index_text):
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
        #boarddropdown.click()

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
        dropdowns = _get_in_dropdowns(driver)
        for dropdown in dropdowns:
            print(dropdown.text)
            print(dropdown)
            if dropdown_text in dropdown.text:
                dropdown.click()
                print("clicked")
                sdrop = dropdown
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
    
    select_dropdown(driver, "Subject", 2)

    time.sleep(1)

    select_dropdown(driver, "Paper", 0)

    time.sleep(0.2)

    select_dropdown(driver, "Paper", 1)

    time.sleep(0.5)

    topics = get_all_dropdowns(driver, "Topics")

    # find_select_dropdown(driver, "Topics", topic)

    # time.sleep(0.5)

    # driver.find_element(By.ID, "get-questions-button").click()
    


    #return driver.current_url

    return topics

    




SUBJECT = "0620"

BASE = "https://markhint.in/topical/igcse/[[SUBJECT]]/results?"

BASE_DIR = "./files/"



def main():
    driver = create_driver()
    try:
        

        
        print(get_topics(driver))


    except Exception as ex:
        print(f"[HEY] encountered {str(type(ex))} {str(ex)}")

    finally:
        time.sleep(8)
        driver.quit()





if __name__ == "__main__":
    main()





