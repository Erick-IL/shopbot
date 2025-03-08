from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

class ShopBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def _find_element(self, object, by=By.CSS_SELECTOR):
        return self.wait.until(EC.presence_of_element_located(by, object))
    
    def _find_elements(self, object, by=By.CSS_SELECTOR):
        return self.wait.until(EC.presence_of_all_elements_located(by, object))