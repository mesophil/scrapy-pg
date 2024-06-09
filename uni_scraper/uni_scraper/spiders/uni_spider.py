import scrapy
from scrapy_playwright.page import PageMethod

class UniSpiderSpider(scrapy.Spider):
    name = "uni_spider"
    # allowed_domains = ["uniqlo.com"]
    # start_urls = ["https://www.uniqlo.com/ca/en/men/outerwear/outerwear-collections"]

    def start_requests(self):
        # wait until elements with a div that has class info are rendered
        url = "https://www.uniqlo.com/ca/en/men/outerwear/outerwear-collections"
        yield scrapy.Request(url, meta={"playwright": True, 
                                        "playwright_include_page" : True, 
                                        "playwright_page_methods" : PageMethod('wait_for_selector', 'div.info'),
                                        }, 
                                        errback=self.errback)

    # idk what benefit asyncio will have here, but we ball
    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        
        for product in response.css("div.info"):

            yield {
                'name': product.css("h2.description.decscription-text.fr-no-uppercase::text").get()
            }
    
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
