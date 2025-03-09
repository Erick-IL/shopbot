
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

class ShopBot():
    def __init__(self):
        options = uc.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def _find_element(self, object, by=By.CSS_SELECTOR):
        """ Tenta procurar um elemento na pagina. Espera até 10 segundos para aparecer na pagina"""
        return self.wait.until(EC.presence_of_element_located((by, object)))
    
    def _find_elements(self, object, by=By.CSS_SELECTOR):
        """ Tenta procurar os elementos na pagina. Espera até 10 segundos para aparecer na pagina"""
        return self.wait.until(EC.presence_of_all_elements_located((by, object)))

    def _get_text(self, product, selector, default="Não disponível"):
        """ Tenta pegar o texto de um elemento. Retorna um valor padrão se não encontrar. """
        try:
            return product.find_element(By.CSS_SELECTOR, selector).text
        except:
            return default

    def _get_attribute(self, product, selector, attribute, default="Não informado"):
        """ Tenta pegar um atributo de um elemento. Retorna um valor padrão se não encontrar. """
        try:
            return product.find_element(By.CSS_SELECTOR, selector).get_attribute(attribute)
        except:
            return default

    def _get_price(self, product):
        """ Tenta pegar o preço de um produto. Retorna um valo padrão se não encontrar """
        try:
            price = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            cents = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
            return f"R$ {price},{cents}"
        except:
            return "Não disponível"