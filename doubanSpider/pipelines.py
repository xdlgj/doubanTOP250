# -*- coding: utf-8 -*-
from doubanSpider.settings import MONGO_IP, MONGO_PORT, MONGO_DB, MONGO_COLLECTION
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class DoubanspiderMongo(object):
	def __init__(self):
		self.mongo_ip = MONGO_IP
		self.mongo_port = MONGO_PORT
		self.mongo_db = MONGO_DB
		self.sheetName = MONGO_COLLECTION
		# 连接数据库
		connect_mongo = pymongo.MongoClient(self.mongo_ip, self.mongo_port)
		# 创建数据库
		myDB = connect_mongo[self.mongo_db]
		# 创建数据表
		self.myCollection = myDB[self.sheetName]
	def process_item(self, item, spider):
		# 插入数据
		self.myCollection.insert(dict(item))
		