import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from openpyxl import Workbook,load_workbook
import os
import json



def load_category (filename):
    category_wb = load_workbook('ikea-link.xlsx', read_only=True)
    category_sw = category_wb.active
    category_info = [[cell.value for cell in sub_category ] for sub_category in category_sw.rows]
    category_info.append(category_info)
    return category_info


def get_info_from_url(browser, sub_category, url):
    global title, title_json
    print(sub_category)
    products_info = []
    browser.get(url + '?page=200')
    time.sleep(10)
    cards = browser.find_elements(By.CLASS_NAME,'per-product-link-wrapper')
    for card in cards :
        product_name = card.find_element(By.CLASS_NAME, "withprice-title").text
        product_desc = card.find_element(By.CLASS_NAME, 'withprice-commit').text
        product_price = card.find_element(By.CLASS_NAME,'withprice-price').text
        print(product_name, product_desc ,product_price)
        product_url = card.get_attribute('href')
        product_code = product_url.split("-")[-1].strip("s/")
        # browser.get(product_url)
        # time.sleep(3)
        # browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/section[2]/div/div[2]/div[1]/span').click()
        # all_spans = driver.find_elements(By.CLASS_NAME, 'item-detail-list')
        # for span in all_spans:
        #     print(span.text)
        # print(package_info)
        # products_images = [img_tag.get_attribute('src') for img_tag in card.find_elements(By.TAG_NAME, "img")]
        # products_info = [sub_category, product_name,
                        # product_desc, product_price,product_url,product_code]
        # products_info += products_images
        # products_info.append(products_images)
        title = browser.title
        title_json = title.replace(" - IKEA",'')
        prod = {
            'sub_category': sub_category,
            'product_info': [{
                'name': product_name,
                'desc': product_desc,
                'price': product_price,
                'product url': product_url,
                'product code': product_code
            }]
        }
        products_info.append(prod)
    with open(f'JSON/{sub_category}/{title_json}.json', 'w') as outfile:
        json.dump(products_info, outfile)
    
    return product_info

def save_info(info, file_name):
    wb = Workbook()
    ws = wb.active
    for row in info:
        ws.append(row)
    wb.save(file_name) 

if __name__ == "__main__":
    path_driver = 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path = path_driver)
    info = load_category('ikea-link.xlsx')
    print(info)
    product_info = []
    cwd = os.getcwd()
    JSON_PATH = os.path.join(cwd,'JSON')
    i = 1
    
    for sub_category in info:
        Path_for_json = os.path.join(JSON_PATH,str(sub_category[0]))
        try:
            os.mkdir(Path_for_json)
        except:
            # directory already exists
            pass
    for sub_category in info:
        print(f" checking and submitting {sub_category[0]} ({i}/{len(info)})")
        
        product_info = get_info_from_url(driver, sub_category[0], sub_category[1])
        print(sub_category[0]+ ' ' + sub_category[1])
        product_info.append(product_info)
        i+=1
    # save_info(product_info, "catergory.xlsx")
    # with open(f'{sub_category[0]} {i}.json', 'w') as outfile:
    #      json.dump(product_info, outfile)
    
    # print(sub_category)
    driver.close()





