# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class CourseCrawlerPipeline:
    def __init__(self):
        self.con = sqlite3.connect('courses.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS courses(
                         url TEXT PRIMARY KEY,
                         name TEXT,
                         topics TEXT,
                         skills TEXT,
                         description TEXT,
                         language TEXT,
                         outcomes TEXT
        )""")

    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO courses VALUES(?,?,?,?,?,?,?)""",
                         (item['url'],item['name'],item['topics'],item['skills'],item['description'],item['language'],item['outcomes']))
        self.con.commit()
        return item
    
    def close_spider(self, spider):
        self.con.close()
