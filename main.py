from main.site.amazon import AmazonScraper



if __name__ == "__main__":
    scraper = AmazonScraper()
    scraper.search_product("SSD NVMe 1TB")