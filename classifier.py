from sklearn.linear_model import LogisticRegression 
import mongocli
import cPickle
class Tool(object):
	#cates=["Auto","Business","Cricket","doc","Education","Entertainment","Health","Lifestyle","National","Politics","Sports","Technology","Top Stories","World"]
	def __init__(self,category="Auto"):
		self.cates=["Auto","Business","Cricket","doc","Education","Entertainment","Health","Lifestyle","National","Politics","Sports","Technology","Top Stories","World"]
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
		self.category = category
		self.tool = Tool(category)
		self.category_anther = self.tool.category_anther
	def getrain(self):
		client = mongocli.MongoCli()
		datas = client.getdata('hinews','article',1000)
		#add positive elements 120
		for data in datas:
			tfidf_vec = cPickle.loads(data['feature'])
			categorys = data['category']
			count = 1
			if self.tool.categoryisok(categorys):
				self.train_X.append(tfidf_vec)
				self.train_Y.append(1)
				count = count + 1
			if count > 120:
				break
		#add negative elements 120 divide into 12 part
		for category in self.category_anther:
			for data in datas:
				tfidf_vec = cPickle.loads(data['feature'])
				categorys = data['category']
				count = 1
				if self.tool.categoryisoks(category,categorys):
					self.train_X.append(tfidf_vec)
					self.train_Y.append(0)
				if count > 10:
					break
		print "train is over..."

		'''
		self.train_X.append([1,0,1,0,0,0,0,0,0,0])
		self.train_Y.append(1)
		self.train_X.append([1,0,0,0,0,0,0,0,0,1])
		self.train_Y.append(1)
		self.train_X.append([1,0,0,1,1,0,0,0,1,1])
		self.train_Y.append(1)
		self.train_X.append([0,0,0,0,0,1,1,1,1,1])
		self.train_Y.append(0)
		self.train_X.append([0,0,0,0,0,0,1,1,1,1])
		self.train_Y.append(0)
		'''
	def trainClassifier(self):
		self.classifier.fit(self.train_X,self.train_Y)
	def getarget(self,text):
		return self.classifier.predict(text)

if __name__ == "__main__":
	cf=Classifier()
	cf.getrain()
	#cf.trainClassifier()
	#target=cf.getarget([0,0,0,0,0,0,0,0,1,0])
	print "game over"
