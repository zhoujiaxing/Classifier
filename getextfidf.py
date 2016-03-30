from sklearn.feature_extraction.text import TfidfVectorizer
class Getextfidf(object):
	def __init__(self):
		self.vectorizer = TfidfVectorizer()
	def setcorpus(self,corpus):
		self.vevtorizer.fit_transform(corpus)
	def getfidf(self,text)
		return:
