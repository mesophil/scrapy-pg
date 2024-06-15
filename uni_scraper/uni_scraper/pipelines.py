# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CleanDescriptionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('desc'):
            adapter['desc'] = adapter['desc'].replace("<br>", " ")
            adapter['desc'] = adapter['desc'].replace(" - ", " ")
            adapter['desc'] = adapter['desc'].replace("- ", " ")
        
        return item

class RoundNumbersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            adapter['price'] = " ".join([str(round(float(adapter['price']), 2)), 'CAD']) # assume it's cad

        if adapter.get('rating'):
            adapter['rating'] = round(float(adapter['rating']), 1)

        return item