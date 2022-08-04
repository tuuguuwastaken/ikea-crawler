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


def get_info_from_url(browser, sub_category, url):

    products_info = []
    browser.get(url + '?page=200')
    time.sleep(10)
    cards = browser.find_elements(By.CLASS_NAME,'product-overview-wrapper' or 'withprice-content ivu-col')
    for card in cards :
        product_name = card.find_element(By.CLASS_NAME, "withprice-title").text
        product_desc = card.find_element(By.CLASS_NAME, 'withprice-commit').text
        product_price = card.find_element(By.CLASS_NAME,'withprice-price').text
        print(product_name, product_desc ,product_price)
        # product_url = card.find_element(By.TAG_NAME,"a").get_attribute('href')
        # product_code = product_url.split("-")[-1].strip("s/")
        products_images = [img_tag.get_attribute('src') for img_tag in card.find_elements(By.TAG_NAME, "img")]
        products_info = [sub_category, product_name,
                        product_desc, product_price,]
        # products_info += products_images
        # products_info.append(products_images)
        prod = {
            'product info': [{
                'name': product_name,
                'desc': product_desc,
                'price':product_price,
            }]
        }
       
        products_info.append(prod)
        
    
    return products_info


if __name__ == "__main__":
    path_driver = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path = path_driver)
    info = load_category('ikea-link.xlsx')
    print(info)
    product_info = []
    i = 1
    for sub_category in info:
        print(f" checking and submitting {sub_category[0]} ({i}/{len(info)})")
        product_info = get_info_from_url(driver, sub_category[0], sub_category[1])
        print(sub_category[0]+ ' ' + sub_category[1])
        product_info.append(product_info)
        i+=1
    with open(f'{sub_category[0]} {i}.json', 'w') as outfile:
        json.dump(product_info, outfile)
    
    # print(sub_category)
    driver.close()





