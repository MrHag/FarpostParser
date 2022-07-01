from typing import Any
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from enum import Enum

class browser_type(Enum):
    CHROME = 1
    FIREFOX = 2

class browser:

    browser_path: str
    home_url: str
    __driver: webdriver.Remote

    __wait: WebDriverWait

    def __init__(self, type: browser_type, browser_path: str, home_url: str = "http://127.0.0.1/"):

        if type == browser_type.CHROME:
            options = webdriver.ChromeOptions()
            options.binary_location = browser_path
            self.__driver = webdriver.Chrome(options=options)
        else:
            options = webdriver.FirefoxOptions()
            options.binary_location = browser_path
            self.__driver = webdriver.Firefox(options=options)

        self.home_url = home_url

        self.__wait = WebDriverWait(self.__driver, timeout=86400.)

    def open_default(self):
        self.__driver.get(self.home_url)

    def open(self, url):
        try:
            self.__driver.get(url)
        except TimeoutException as e:
            print("Timeout: ", e)
            self.open(url)

    def page_source(self) -> str:
        return self.__driver.page_source
    
    def current_url(self) -> str:
        return self.__driver.current_url

    def find_element_by_class_name(self, name: str):
        self.__driver.find_element_by_class_name(name)
    
    def find_element_by_id(self, id: str):
        self.__driver.find_element_by_id(id)

    def get_cookies(self):
        return self.__driver.get_cookies()

    def delete_cookies(self):
        self.__driver.delete_all_cookies()

    def check_browser(self) -> bool:
        driver = self.__driver
        self.open_default()
        bwait = WebDriverWait(driver, 5)
        try:
            bwait.until(EC.url_to_be(self.home_url))
        except TimeoutException:
            return False
        finally:
            driver.delete_all_cookies()
        return True

    def wait_for_url(self, url):
        self.wait_util(EC.url_to_be(url))

    def wait_util(self, method: Any):
        wait = self.__wait
        try:
            wait.until(method)
        except TimeoutException:
            return
    
    def wait_util_not(self, method: Any):
        wait = self.__wait
        try:
            wait.until_not(method)
        except TimeoutException:
            return

    def execute_script(self, script: str):
        return self.__driver.execute_script(script)

    def quit(self):
        self.__driver.quit()