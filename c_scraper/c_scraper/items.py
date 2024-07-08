# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AberItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    product_id = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()

