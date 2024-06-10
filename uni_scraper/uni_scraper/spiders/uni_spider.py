import scrapy
from uni_scraper.items import UniItem

class UniSpiderSpider(scrapy.Spider):
    name = "uni_spider"

    def start_requests(self):
        # wait until elements with a div that has class info are rendered
        url = "https://www.uniqlo.com/ca/en/men/tops/tops-collections"
        yield scrapy.Request(url, meta={"playwright": True,
                                        }
                                        )

    def parse(self, response):
        # yield {"url": response.url}

        # product_item = UniItem()

        for product in response.css("div.fr-product-card.default"):
            # product_item['name'] = product.css("h2.description.decscription-text.fr-no-uppercase::text").get()
            # product_item['price'] = 0
            # product_item['url'] = "a"
            # yield product_item
            yield {'name' : product.css("h2.description.decscription-text.fr-no-uppercase::text").get()}