# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class CleanDescriptionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('desc'):
            adapter['desc'] = adapter['desc'].replace("<br>", " ")
            adapter['desc'] = adapter['desc'].replace(" - ", " ")
            adapter['desc'] = adapter['desc'].replace("- ", " ")

            adapter['desc'] = re.sub(r'\s+', ' ', adapter['desc'])
        
        return item

class RoundNumbersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            adapter['price'] = str(round(float(adapter['price']), 2)) # assume it's cad

        if adapter.get('rating'):
            adapter['rating'] = round(float(adapter['rating']), 1)

        return item
    
class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # may need to amend this later to be more discriminatory
        # product id avoids only the exact same item
        # if the product is listed in two colours, this may not trigger the duplicates filter
        if adapter['product_id'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['product_id'])
            return item