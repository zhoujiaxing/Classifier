from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer 
import mongocli
import cPickle
import sys
reload(sys)  
sys.setdefaultencoding('utf8') 
class Tool(object):
	#cates=["Auto","Business","Cricket","doc","Education","Entertainment","Health","Lifestyle","National","Politics","Sports","Technology","Top Stories","World"]
	def __init__(self,category="Auto"):
		self.cates=["Auto","Business","Cricket","Education","Entertainment","Health","Lifestyle","National","Politics","Sports","Technology","Top Stories","World"]
		self.category = category
		self.category_anther = self.getanther()
	def getanther(self):
		anther=[]
		for cate in self.cates:
			if cate!=self.category:
				anther.append(cate)
		return anther
	def categoryisok(self,categorys):
		if self.category in categorys:
			return True
		return False
	def categoryisoks(self,category,categorys):
		if self.category not in categorys and category in categorys:
			return True
		return False
class Classifier(object):
	def __init__(self,category="Auto"):
		self.classifier = LogisticRegression()
		self.vectorizer = TfidfVectorizer()
		self.train_X = []
		self.train_Y = []
		self.train_swp = []
		self.train_text = []
		self.category = category
		self.tool = Tool(category)
		self.category_anther = self.tool.category_anther
	def trainclassifier(self):
		client = mongocli.MongoCli()
		datas = client.getdata('hinews','article',80000)
		#add positive elements 120
		count = 1
		for data in datas:
			#tfidf_vec = cPickle.loads(data['feature']).toarray()[0]
			categorys = data['category']
			text = data['text']
			if self.tool.categoryisok(categorys):
				self.train_swp.append(text)
				self.train_Y.append(1)
				if count < 11:
					self.train_text.append(text)
				count = count + 1
			if count > 120:
				print ("%s is over....")%self.category
				break
		print count
		#print text.encode('utf8')
		#add negative elements 120 divide into 12 part
		for category in self.category_anther:
			count = 1
			for data in datas:
				#tfidf_vec = cPickle.loads(data['feature']).toarray()[0]
				categorys = data['category']
				text = data['text']
				if self.tool.categoryisoks(category,categorys):
					self.train_swp.append(text)
					self.train_Y.append(0)
					self.train_text.append(text)
					count = count + 1
				if count > 10:
					print("%s is over.....")%category
					break
			print count
		self.vectorizer.fit_transfrom(self.train_text)
		for text in self.train_swp:
			ifidf = self.vectorizer.transfrom(text)
			array = tfidf.toarray()[0]
			self.train_X.append(array)
		self.classifier.fit(self.train_X,self.train_Y)
		#self.vectorizer.fit_transform(self.train_text)
		print "train is over...."
	def getarget(self,text):
		tfidf = self.vectorizer.transform(text)
		array = tfidf.toarray()[0]
		return self.classifier.predict(array)
'''
if __name__ == "__main__":
	cf=Classifier()
	cf.trainclassifier()
	#target=cf.getarget([0,0,0,0,0,0,0,0,1,0])
	print "game over"
'''
