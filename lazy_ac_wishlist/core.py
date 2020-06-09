import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoAlertPresentException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from lazy_ac_wishlist.version import __version__

Options.headless = True
PATH_FIREFOX = Path(os.getcwd(), "firefox")

fp = webdriver.FirefoxProfile(
    "/Users/perez/Library/Application Support/Firefox/Profiles/1rasxmm5.default-release"
)

driver = webdriver.Firefox(
    executable_path=str(PATH_FIREFOX / "geckodriver"),
    service_log_path=str(PATH_FIREFOX / "gecko.log"),
    firefox_profile=fp,
)
# /html/body/div/div/div[1]/div[2]/div/div[2]/div[4]/div[2]/span
driver.implicitly_wait(20)

WISHLIST = "Wallpapers"
RUGS = False

next_page = None


def main():
    driver.get("https://nookazon.com/products/furniture/wallpaper")

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
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, './/a[@class="sc-AxjAm kCLLqI item-img"]')
            )
        )
        time.sleep(1)
        link = (
            tmp[i]
            .find_element_by_xpath('.//a[@class="sc-AxjAm kCLLqI item-img"]')
            .get_attribute("href")
        )
        addToWishlist(link)


def getChildren():
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "row"))
        )
        row = driver.find_element_by_class_name("row")
        children = row.find_elements_by_class_name("col-sm-3")
        return children
    except TimeoutException:
        driver.quit()
        quit()


def addToWishlist(link: str) -> None:
    driver.get(link)
    try:
        name = _getItemName()
        if not _canCraft() and _canBuy():
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div/div[1]/div[2]/div/div[2]/div[4]/div[1]/div/div[2]",
                    )
                )
            ).click()
            ActionChains(driver).pause(1).send_keys(WISHLIST).pause(1).send_keys(
                Keys.ENTER
            ).pause(1).perform()
        else:
            print(f"Did NOT add {name}")
    except TimeoutException:
        driver.quit()
        print("unable to add this item")
        raise
    except:
        driver.quit()
        raise

    try:
        driver.back()
    except UnexpectedAlertPresentException:
        time.sleep(1)
        driver.back()


def _getItemName() -> str:
    try:
        item = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]',
                    )
                )
            )
            .text
        )
        return item
    except TimeoutException("Unable to get item name"):
        raise


def _canBuy() -> bool:
    try:
        price = (
            WebDriverWait(driver, 3)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/div[3]/span[2]',
                    )
                )
            )
            .text
        )
        text = price.split(":")

        try:
            if text[0] == "Buy":
                return True
            else:
                return False
        except:
            raise
    except TimeoutException:
        return False


def _canCraft() -> bool:
    try:
        obtained = (
            WebDriverWait(driver, 5)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/div[4]',
                    )
                )
            )
            .text
        )
        text = obtained.split(":")

        try:
            text_stripped = text[1].lstrip()
        except IndexError:
            return False

        if text_stripped == "Crafting":
            return True
        if text_stripped == "Saharah" and not RUGS:
            return True
        else:
            return False
    except TimeoutException:
        raise


def _hasNextPage() -> bool:
    global next_page
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#root > div > div:nth-child(1) > div.items > div > div.page-bar > div.next-btn.link-btn",
                )
            )
        )
        next_page = driver.find_element_by_css_selector(
            "#root > div > div:nth-child(1) > div.items > div > div.page-bar > div.next-btn.link-btn"
        )
        return True
    except TimeoutException:
        return False


if __name__ == "__main__":
    main()
    driver.quit()
