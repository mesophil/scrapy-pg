import scrapy
from uni_scraper.items import UniItem
from uni_scraper.generate_urls import urls
from scrapy_playwright.page import PageMethod

class UniSpiderSpider(scrapy.Spider):
    name = "uni_spider"

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url, 
                                 meta={"playwright": True, 
                                       "playwright_include_page": True,
                                       }, 
                                 callback=self.parse)

    async def parse(self, response):
        page = response.meta["playwright_page"]
        page.set_default_timeout(1000)

        try:
            # maybe use class fr-load-more
            # but then how to target the <a>? the div is inside the link rather than containing it
            # problem right now is that w12 might be used elsewhere lol
            while button := page.locator("//div[contains(@class,'w12')]/a"):
                await button.scroll_into_view_if_needed()
                await button.click()
        except:
            pass

        # await page.close()

        product_item = UniItem()
        for product in response.css("div.fr-product-card.default"):
            product_item['name'] = product.css(".description.fr-no-uppercase::text").get()
            product_item['price'] = product.css("span.fr-price-currency>span::text").get()
            product_item['image'] = product.css("img.thumb-img::attr(src)").get()
            yield product_item