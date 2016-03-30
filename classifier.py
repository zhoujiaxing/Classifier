from sklearn.linear_model import LogisticRegression 
import mongocli
import cPickle
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
		self.train_X = []
		self.train_Y = []
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
			tfidf_vec = cPickle.loads(data['feature']).toarray()[0]
			categorys = data['category']
			text = data['text']
			count = 1
			if self.tool.categoryisok(categorys):
				self.train_X.append(tfidf_vec)
				self.train_Y.append(1)
				self.train_text.append(text)
				count = count + 1
			if count > 120:
				print ("%s is over....")%self.category
				break
		print count
		#add negative elements 120 divide into 12 part
		for category in self.category_anther:
			count = 1
			for data in datas:
				tfidf_vec = cPickle.loads(data['feature']).toarray()[0]
				categorys = data['category']
				text = data['text']
				count = 1
				if self.tool.categoryisoks(category,categorys):
					self.train_X.append(tfidf_vec)
					self.train_Y.append(0)
					self.train_text.append(text)
				if self.tool.categoryisoks(category,categorys):
					self.train_X.append(tfidf_vec)
					self.train_Y.append(0)
					count = count + 1
				if count > 10:
					print("%s is over.....")%category
					break
		print "train is over..."
		print text
	def trainClassifier(self):
			print count
		self.classifier.fit(self.train_X,self.train_Y)
		print "train is over...."
	def getarget(self,text):
		return self.classifier.predict(text)

if __name__ == "__main__":
	cf=Classifier()
	cf.trainclassifier()
	#target=cf.getarget([0,0,0,0,0,0,0,0,1,0])
	print "game over"
