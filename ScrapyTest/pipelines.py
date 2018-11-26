# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from ScrapyTest.settings import monodb_host,monodb_port,monodb_db_name,monodb_tb_name
class ScrapytestPipeline(object):
    def __init__(self):
        host = monodb_host
        port = monodb_port
        dbname = monodb_db_name
        sheetname = monodb_tb_name
        client = pymongo.MongoClient(host=host,port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
