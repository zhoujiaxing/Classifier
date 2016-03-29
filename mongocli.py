import pymongo
from pymongo import MongoClient
class MongoCli(object):
	def __init__(self):
		self.client = MongoClient('mongodb://54.169.111.247')
	def getdata(self,database,collection,num):
		db = self.client[database]
		coll = db[collection]
		return coll.find().limit(num)
