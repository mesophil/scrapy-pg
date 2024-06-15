import scrapy
from uni_scraper.items import UniItem
from uni_scraper.generate_urls import read_urls
import logging
import json

logging.basicConfig(filename='my.log', encoding='utf-8', level=logging.DEBUG)

class UniSpiderJson(scrapy.Spider):
    name = "uni_spider"
    allowed_domains = ["uniqlo.com"]
    start_urls = read_urls()

    def parse(self, response):
        data = json.loads(response.text)

        product_item = UniItem()

        if not data["result"]:
            yield 'null'

        for item in data["result"]["items"]:
            product_item['name'] = item['name']
            product_item['product_id'] = item['productId']
            product_item['gender'] = item['genderName']
            product_item['desc'] = item['longDescription']

            product_item['composition'] = item['composition']

            if item['prices']['promo']:
                product_item['price'] = " ".join([item['prices']['promo']['value'], item['prices']['promo']['currency']['code']])
            elif item['prices']['base']:
                product_item['price'] = " ".join([item['prices']['base']['value'], item['prices']['base']['currency']['code']])
            else:
                product_item['price'] = 'Null'

            product_item['rating'] = item['rating']['average'] if item['rating'] else 'Null'
            product_item['size_chart'] = item['sizeChartUrl']
            product_item['washing_info'] = item['washingInformation']

            yield product_item
        