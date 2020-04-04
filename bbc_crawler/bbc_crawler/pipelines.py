# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import json

class BbcCrawlerPipeline(object):

    def __init__(self):
        print('__init__ Start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        self.client = MongoClient(
            host = '192.168.111.139',
            username = 'root',
            password = 'tlsdbstjr1+',
            port = 27017,
            authSource = 'admin',
        )

        self.collection = self.client['news'].articles

    def process_item(self, item, spider):

        print('PipeLine Start!!!!!!!!!!!!!!!')
        with open('items.json', 'w') as f:
            f.write(json.dumps(item))

        for i in range(len(item)):
            self.collection.insert(dict(item[str(i)]))

        return item
