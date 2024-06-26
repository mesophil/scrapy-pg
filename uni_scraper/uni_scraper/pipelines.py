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

        for s in ['desc', 'washing_info', 'composition']:

            if adapter.get(s):
                adapter[s] = adapter[s].replace("<br>", " ")
                adapter[s] = adapter[s].replace(" - ", " ")
                adapter[s] = adapter[s].replace("- ", " ")

                adapter[s] = re.sub(r'\s+', ' ', adapter[s])
        
        return item

class RoundNumbersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            adapter['price'] = str('{:.2f}'.format(round(float(adapter['price']), 2)))

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