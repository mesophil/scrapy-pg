# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UniItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    product_id = scrapy.Field()
    gender = scrapy.Field()
    desc = scrapy.Field()
    img = scrapy.Field()
    composition = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    size_chart = scrapy.Field()
    washing_info = scrapy.Field()
