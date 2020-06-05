import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
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
    total_children = int(len(children))
    link = children[0].find_element_by_xpath('.//a[@class="sc-AxjAm kCLLqI item-img"]').get_attribute('href')

    addToWishlist(link)

def addToWishlist(link: str) -> None:
    driver.get(link)
    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.add-wishlist-select > div:nth-child(1)')))
        menu = driver.find_element_by_css_selector('.add-wishlist-select > div:nth-child(1)')
    except TimeoutError:
        driver.quit()
        raise
    except:
        driver.quit()
        raise

    ActionChains(driver).move_to_element(menu).click().pause(1).send_keys('test').pause(1).send_keys(Keys.ENTER).pause(1).perform()

    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        pass
    finally:
        driver.back()

# TODO: loop through children

# TODO: in each child, open in new tab
    #TODO: check if craftable OR NOT purchasable
    
    #TODO: otherwise, add to wishlist 'test'

if __name__ == '__main__':
    getChildren()
    
    driver.quit()