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

        categories = []
        for category in data["result"]["aggregations"]["tree"]["classes"]:
            categories.append(category["name"])

        product_item['category'] = categories

        for item in data["result"]["items"]:
            product_item['name'] = item['name']
            product_item['product_id'] = item['productId']
            product_item['gender'] = item['genderName']
            product_item['desc'] = item['longDescription']

            product_item['img'] = item['images']['main'][0]['url']

            product_item['composition'] = item['composition']

            if item['prices']['promo']:
                product_item['price'] = item['prices']['promo']['value']
            elif item['prices']['base']:
                product_item['price'] = item['prices']['base']['value']
            else:
                product_item['price'] = None

            product_item['rating'] = item['rating']['average'] if item['rating'] else None

            if item['sizeInformation']:
                product_item['size_chart'] = item['sizeInformation']
            else:
                product_item['size_chart'] = item['sizeChartUrl']

            product_item['washing_info'] = item['washingInformation']

            yield product_item
        