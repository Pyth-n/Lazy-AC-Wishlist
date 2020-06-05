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

def getChildren() -> None:
    driver.get('https://nookazon.com/products/furniture/wallpaper')

    # TODO: find parent with an array of children
    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'row')))
        row = driver.find_element_by_class_name('row')
        children = row.find_elements_by_class_name('col-sm-3')
    except TimeoutException:
        driver.quit()

    # # TODO: set total number of children
    for i, child in enumerate(children):
        link = child.find_element_by_xpath('.//a[@class="sc-AxjAm kCLLqI item-img"]').get_attribute('href')
        addToWishlist(link)

    _getLoadButton()

def addToWishlist(link: str) -> None:
    driver.get(link)
    try:
        time.sleep(1)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/div[2]'))).click()
        ActionChains(driver).pause(1).send_keys('test').pause(1).send_keys(Keys.ENTER).pause(1).perform()
    except TimeoutException as e:
        driver.quit()
        raise
    except:
        driver.quit()
        raise

    try:
        driver.back()
    except UnexpectedAlertPresentException as e:
        time.sleep(1)
        driver.back()
        
def _getLoadButton():
    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#root > div > div:nth-child(1) > div.items > div > div.page-bar > div.next-btn.link-btn'))).click()
    except TimeoutException:
        driver.quit()
        raise
# TODO: loop through children

# TODO: in each child, open in new tab
    #TODO: check if craftable OR NOT purchasable
    
    #TODO: otherwise, add to wishlist 'test'

if __name__ == '__main__':
    getChildren()
    driver.quit()