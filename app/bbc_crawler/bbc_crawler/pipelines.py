# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import json
from .spiders.articlescrawler import ArticleSpider

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

        self.collection = self.client['news'].articles_app

    def process_item(self, item, spider):
        print('Starting!!!!!!!!! Pipeline process_item Function')
        for i in range(len(item)):
            self.collection.insert(dict(item[str(i)]))

        return item

    def close_spider(self, spider):
        print('Close_spider!!!!!!!!!!!!!!!!!!!!!!!!')
        for i in range(len(ArticleSpider.articles)):
            self.collection.insert(dict(ArticleSpider.articles[str(i)]))
        self.client.close()
