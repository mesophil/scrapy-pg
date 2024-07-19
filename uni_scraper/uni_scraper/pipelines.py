# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re
import uni_scraper.config as config

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
    
    def open_spider(self, spider):
        # Open the database connection and cursor when the spider starts
        try:
            self.connection = psycopg2.connect(host=config.host,
                                               dbname=config.dbname,
                                               user=config.username,
                                               password=config.username,
                                               port=config.port)
            self.curr = self.connection.cursor()
            print("Database connection opened.")

        except BaseException as e:
            print(f"Error opening database connection: {e}")

        # create staging DB
        try:
            self.create_staging()
            print("Staging DB created.")
        
        except BaseException as e:
            print(f"Could not create staging database: {e}")


    def close_spider(self, spider):

        # merge tables
        try:
            self.merge_tables()
            print("Tables merged.")
        
        except BaseException as e:
            print(f"Could not merge staging table into prod: {e}")

        # Commit any remaining transactions and close the connection and cursor when the spider finishes
        try:
            if self.connection:
                self.connection.commit()
                self.curr.close()
                self.connection.close()
                print("Database connection closed.")

        except BaseException as e:
            print(f"Error closing database connection: {e}")



    def create_staging(self):
        self.curr.execute("""CREATE TEMP TABLE StagingProducts (
                                    gender VARCHAR(16),
                                    category VARCHAR(32),
                                    name VARCHAR(128),
                                    product_id VARCHAR(32) PRIMARY KEY,
                                    img TEXT,
                                    price VARCHAR(16),
                                    rating VARCHAR(16),
                                    composition TEXT,
                                    product_info TEXT,
                                    washing_info TEXT,
                                    size_chart TEXT
                                    ); """)
        return
    
    def process_item(self, item, spider):

        # write all items to staging DB
        try:
            self.curr.execute(""" INSERT INTO StagingProducts (
                              gender, category, name, product_id, img, price, rating, composition, product_info, washing_info, size_chart
                              ) VALUES (
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
    
    def merge_tables(self):
        self.update_prod()
        self.add_new_rows()
        self.delete_obselete_rows()
        return


    def update_prod(self):
        self.curr.execute("""
                          UPDATE UniProducts t
                          SET
                            gender = s.gender,
                            category = s.category,
                            name = s.name,
                            img = s.img,
                            price = s.price,
                            rating = s.rating,
                            composition = s.composition,
                            product_info = s.product_info,
                            washing_info = s.washing_info,
                            size_chart = s.size_chart
                          FROM StagingProducts s
                          WHERE t.product_id = s.product_id;
                            """
                          )
        
    def add_new_rows(self):
        self.curr.execute("""
                          INSERT INTO UniProducts (gender, category, name, product_id, img, price, rating, composition, product_info, washing_info, size_chart)
                          SELECT s.gender, s.category, s.name, s.product_id, s.img, s.price, s.rating, s.composition, s.product_info, s.washing_info, s.size_chart
                          FROM StagingProducts s
                          LEFT JOIN UniProducts t ON s.product_id = t.product_id
                          WHERE t.product_id IS NULL;
                          """
                          )

    def delete_obselete_rows(self):
        self.curr.execute("""
                          DELETE FROM UniProducts
                          WHERE product_id NOT IN (SELECT product_id FROM StagingTable);
                          """
                          )

    