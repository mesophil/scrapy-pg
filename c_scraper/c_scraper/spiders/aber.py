import scrapy
from c_scraper.items import AberItem

class AberSpider(scrapy.Spider):
    name = "aber"
    allowed_domains = ["abercrombie.com"]
    start_urls = ["https://www.abercrombie.com/shop/ca/mens-tops--1"]

    def parse(self, response):
        products = response.css('div.catalog-productCard-module__template product-template')
        
        aber_item = AberItem()

        for product in products:

            product_id = product.css('a.catalog-productCard-module__product-content-link::attr(href)').get()
            
            aber_item['product_id'] = product_id
            aber_item['img'] = product.css('div.catalog-productCard-module__product-image-section > div > a > img::attr(src)').get()

            aber_item['name'] = product.css('span.productName::text').get()

            aber_item['price'] = product.css('span.price::text').get() # this is in USD

            aber_item['gender'] = product_id.split('/')[4]
            aber_item['category'] = product_id.split('/')[6]

            yield aber_item
