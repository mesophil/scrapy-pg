import scrapy
from uni_scraper.items import UniItem
from uni_scraper.generate_urls import urls

class UniSpiderSpider(scrapy.Spider):
    name = "uni_spider"

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        product_item = UniItem()

        for product in response.css("div.fr-product-card.default"):
            product_item['name'] = product.css(".description.fr-no-uppercase::text").get()
            product_item['price'] = product.css("span.fr-price-currency>span::text").get()
            product_item['image'] = product.css("img.thumb-img::attr(src)").get()
            yield product_item