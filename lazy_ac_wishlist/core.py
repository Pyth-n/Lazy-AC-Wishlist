import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from lazy_ac_wishlist.version import __version__

Options.headless = True
PATH_FIREFOX = Path(os.getcwd(), 'firefox')

fp = webdriver.FirefoxProfile('/Users/perez/Library/Application Support/Firefox/Profiles/1rasxmm5.default-release')

driver = webdriver.Firefox(
    executable_path=str(PATH_FIREFOX / 'geckodriver'),
    service_log_path=str(PATH_FIREFOX / 'gecko.log'),
    firefox_profile=fp)
# /html/body/div/div/div[1]/div[2]/div/div[2]/div[4]/div[2]/span
driver.implicitly_wait(20)

next_page = None

def main():
    driver.get('https://nookazon.com/products/furniture/wallpaper?page=10')
    
    while _hasNextPage():
        renderPage()
        time.sleep(1.0)
        next_page.click()
        time.sleep(1)
        driver.get(driver.current_url)
        time.sleep(1)

    if not _hasNextPage():
        time.sleep(1)
        driver.get(driver.current_url)
        time.sleep(1)
        renderPage()

def renderPage():
    tmp = getChildren()
    i = 0
    for i in range(i, len(tmp)):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/a[@class="sc-AxjAm kCLLqI item-img"]')))
        link = tmp[i].find_element_by_xpath('.//a[@class="sc-AxjAm kCLLqI item-img"]').get_attribute('href')
        addToWishlist(link)

def getChildren():
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'row')))
        row = driver.find_element_by_class_name('row')
        children = row.find_elements_by_class_name('col-sm-3')
        return children
    except TimeoutException:
        driver.quit()
        quit()
   

def addToWishlist(link: str) -> None:
    driver.get(link)
    try:
        time.sleep(1)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/div[2]'))).click()
        ActionChains(driver).pause(1).send_keys('test').pause(1).send_keys(Keys.ENTER).pause(1).perform()
    except TimeoutException as e:
        driver.quit()
        print('unable to add this item')
        raise
    except:
        driver.quit()
        raise

    try:
        driver.back()
    except UnexpectedAlertPresentException as e:
        time.sleep(1)
        driver.back()

def _hasNextPage() -> bool:
    global next_page
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div:nth-child(1) > div.items > div > div.page-bar > div.next-btn.link-btn')))
        next_page = driver.find_element_by_css_selector('#root > div > div:nth-child(1) > div.items > div > div.page-bar > div.next-btn.link-btn')
        return True
    except TimeoutException:
        return False


# TODO: in each child, open in new tab
    #TODO: check if craftable OR NOT purchasable
    
    #TODO: otherwise, add to wishlist 'test'

if __name__ == '__main__':
    main()
    driver.quit()