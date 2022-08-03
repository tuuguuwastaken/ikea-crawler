import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from openpyxl import Workbook,load_workbook
import json

def load_category (filename):
    category_wb = load_workbook('ikea-link.xlsx', read_only=True)
    category_sw = category_wb.active
    category_info = [[cell.value for cell in sub_category ] for sub_category in category_sw.rows]
    category_info.append(category_info)
    return category_info

def get_info(browser, sub, url):
    products_info = []
    browser.get(url + "?page=200")
    time.sleep(10)
    cards = browser.find_elements(By.CLASS_NAME,'product-overview-wrapper' or 'withprice-content ivu-col')
    for card in cards:
        product_name = card.find_element(By.CLASS_NAME, "withprice-title").text
        product_desc = card.find_element(By.CLASS_NAME, 'withprice-commit').text
        product_price = card.find_element(By.CLASS_NAME,'withprice-price').text
        print(product_name, product_desc ,product_price)
if __name__ == "__main__":
    print('starting now')
    path_driver = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path = path_driver)
    info = load_category('ikea-link.xlsx')
    product_info = []
    i= 1;
    for sub_category in info:
        print(f" checking and submitting {sub_category[0]} ({i}/{len(info)})")
        get_info(driver, sub_category[0], sub_category[1])
        i+=1
