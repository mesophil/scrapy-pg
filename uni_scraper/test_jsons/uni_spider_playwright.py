import scrapy
from uni_scraper.items import UniItem
from uni_scraper.generate_urls import urls
from scrapy_playwright.page import PageMethod
import logging

logging.basicConfig(filename='my.log', encoding='utf-8', level=logging.DEBUG)

class UniSpiderPlaywright(scrapy.Spider):
    name = "uni_spider_playwright"

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url, 
                                 meta={"playwright": True, 
                                       "playwright_include_page": True,
                                       }, 
                                 callback=self.parse)

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page.set_default_timeout(5000)
        await page.wait_for_selector('.description.fr-no-uppercase')

        # with open('page1.html', 'wb') as html_file:
        #     html_file.write(response.body)

        try:
            while button := page.locator("div.w12>a"):
                logging.info("LOCATED BUTTON")
                await button.click()
                await page.wait_for_selector('.description.fr-no-uppercase')
                await page.wait_for_load_state()
        except:
            logging.info("COULD NOT LOCATE BUTTON")
            pass

        with open('page2.html', 'wb') as html_file:
            html_file.write(response.body)

        await page.close()

        logging.info("Page done")

        product_item = UniItem()
        for product in response.css("div.fr-product-card.default"):
            product_item['name'] = product.css(".description.fr-no-uppercase::text").get()
            product_item['price'] = product.css("span.fr-price-currency>span::text").get()
            product_item['image'] = product.css("img.thumb-img::attr(src)").get()
            yield product_item