from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from main.bot.search_bot import ShopBot
from PIL import Image
import pytesseract
import requests
import json
import time
import os


class AmazonScraper:
    def __init__(self):
        self.bot = ShopBot()
        self.wait = WebDriverWait(self.bot.driver, 10)
    
    def pass_captcha(self):
        try: 
            while True:
                time.sleep(5)
                image_to_solve = self.bot._find_element("div.a-box-inner div.a-row.a-text-center img").get_attribute("src")
                request = requests.get(image_to_solve)
                with open('main/site/temp/image.png', 'wb') as file:
                    file.write(request.content)
                image = Image.open('main/site/temp/image.png')
                print("imagem salva")
                text = pytesseract.image_to_string(image)
                print(text)

                input_box = self.bot._find_element('input.a-span12')
                input_box.send_keys(text)
                time.sleep(2)
                submit_button = self.bot._find_element('button.a-button-text')
                submit_button.click()
        except Exception as e:
            os.remove('main/site/temp/image.png')
            print(e)

    def search_product(self, product):
        self.bot.driver.get("https://www.amazon.com.br/")       
        self.pass_captcha()
        #input('enter para continuar')

        search_box: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#twotabsearchtextbox")))
        search_box.send_keys(product)

        search_submit: WebElement = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#nav-search-submit-button")))
        search_submit.click()

        time.sleep(5)

        products = self.bot._find_elements("div[data-component-type='s-search-result']")
        product_list = []

        for product in products:
            try:
                title = self.bot._get_text(product, "h2 span")
                link = self.bot._get_attribute(product, "a", "href")
                image = self.bot._get_attribute(product, "img.s-image", "src")
                price = self.bot._get_price(product)
                rating = self.bot._get_attribute(product, "div.a-row.a-size-small a ", "aria-label")
                num_reviews = self.bot._get_text(product, "span.a-size-base.s-underline-text", "0")
                shipping = self.bot._get_attribute(product, "div.a-row.s-align-children-center span", "aria-label", "Não informado")
                try:
                    freight = product.find_element(By.CSS_SELECTOR, 
                    "div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small > div:nth-child(4) > div > div:nth-child(2) > span > span").text
                except:
                    freight = "Não informado"

                product_list.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "image": image,
                    "rating": rating,
                    "num_reviews": num_reviews,
                    "shipping": shipping,
                    "freight": freight
                })

            except Exception as e:
                print(f"Erro ao processar produto: {e}")

        with open("main/json/amazon_products.json", "w", encoding="utf-8") as f:
            json.dump(product_list, f, ensure_ascii=False, indent=4)

        print("Dados salvos em 'amazon_products.json'!")
        self.bot.driver.quit()

