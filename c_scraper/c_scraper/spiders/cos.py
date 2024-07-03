import scrapy
from c_scraper.items import CosItem

class CosSpider(scrapy.Spider):
    name = "cos"
    allowed_domains = ["cos.com"]
    start_urls = ["https://www.cos.com/en/men/t-shirts.html"]

    def parse(self, response):
        products = response.css('.o-product')
        
        cos_item = CosItem()

        for product in products:

            product_id = product.css('a.a-link.no-styling::attr(href)').get()
            
            cos_item['product_id'] = product_id
            cos_item['img'] = product.css('img.a-image.default-image.ResolveComplete::attr(src)').get() # it's joever the image doesnt exist in jpg

            cos_item['name'] = product.css('span.productName::text').get()

            cos_item['price'] = product.css('span.price::text').get() # this is in USD

            cos_item['gender'] = product_id.split('/')[4]
            cos_item['category'] = product_id.split('/')[6]

            yield cos_item
