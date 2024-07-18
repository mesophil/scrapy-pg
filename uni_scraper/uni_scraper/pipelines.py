# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re

import psycopg2

class CleanDescriptionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        for s in ['product_info', 'washing_info', 'composition']:

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
        
class SaveToPostgresPipeline:
    
    def __init__(self) -> None:
        pass

    def open_spider(self, spider):
        # Open the database connection and cursor when the spider starts
        try:
            self.connection = psycopg2.connect(host='aws-0-us-east-1.pooler.supabase.com',
                                               dbname='postgres',
                                               user='postgres.akuzqmqccgzywodqtglx',
                                               password='DCtcYwoC^m*aCAJ&#&t6vwE@zYk5s4LF',
                                               port=6543)
            self.curr = self.connection.cursor()
            print("Database connection opened.")

        except BaseException as e:
            print(f"Error opening database connection: {e}")

    def close_spider(self, spider):
        # Commit any remaining transactions and close the connection and cursor when the spider finishes
        try:
            if self.connection:
                self.connection.commit()
                self.curr.close()
                self.connection.close()
                print("Database connection closed.")

        except BaseException as e:
            print(f"Error closing database connection: {e}")
    
    def process_item(self, item, spider):
        try:
            self.curr.execute(""" insert into products (
                              gender, category, name, product_id, img, price, rating, composition, product_info, washing_info, size_chart
                              ) values (
                              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                              )""", (
                                item["gender"],
                                item["category"],
                                item["name"],
                                item["product_id"],
                                item["img"],
                                item["price"],
                                item["rating"],
                                item["composition"],
                                item["product_info"],
                                item["washing_info"],
                                item["size_chart"]
                                )
                            )

        except BaseException as e:
            print(f"Error storing item: {e}")
            self.connection.rollback()

        return item