#!/usr/bin/python

import utils
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class SeleniumController():
    def __init__(self):
        utils.init_logging()
        self.driver = utils.init_webdriver()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()
        self.driver.quit()
    
    @utils.driver_time("looking for element", "found element after")
    def wait_for_element(self, id, length=10) -> None:
        WebDriverWait(self.driver, length).until(EC.presence_of_element_located((By.ID, id)))
   
    @utils.driver_time("sending keys for element", "sent keys after")
    def send_keys(self, id, keys) -> None:
        self.driver.find_element(By.ID, id).send_keys(keys)

    @utils.driver_time("clicking element", "clicked after")
    def click_element(self, id) -> None:
        self.driver.find_element(By.ID, id).click()

    def select_list_by_index(self, id, index) -> None:
        Select(self.driver.find_element(By.ID, id)).select_by_index(index)

    @utils.driver_time("looking for element", "found element after")
    def find_element_xpath(self, path) -> WebElement:
        return self.driver.find_element(By.XPATH, path)

    @utils.driver_time("loading page", "loaded page after")
    def load_page(self, url) -> None:
        self.driver.get(url)
       


