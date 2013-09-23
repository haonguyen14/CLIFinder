import lucene

from dogpile.cache import make_region
from Caching import MemoryBackendProxy, key_generator

from org.apache.pylucene.queries import PythonCustomScoreQuery, PythonCustomScoreProvider
from org.apache.lucene.index import Term
from org.apache.lucene.search import TermQuery, BooleanQuery, BooleanClause

from django.conf import settings


CACHE = make_region(function_key_generator = key_generator).configure('dogpile.cache.memory', wrap = [MemoryBackendProxy])


class CommandScoreProvider(PythonCustomScoreProvider):

	def __init__(self, context, strQuery):

		PythonCustomScoreProvider.__init__(self, context)

		self.mStrQuery = strQuery

		################# Config quick searcher ############
		self.mIndexReader = settings.ADMINS_ENGINE.mIndexReader
		self.mIndexSearcher = settings.ADMINS_ENGINE.getIndexSearcher()
		self.mQueryParser = settings.ADMINS_ENGINE.getQueryParser()
		##################################################
		self.mQuery = self.mQueryParser.parse(self.mStrQuery)

	def customScore(self, doc, subQueryScore, valSrcScore):
		
		docObject = self.mIndexReader.document(doc)
		id = docObject.get('id')
		name = docObject.get('name').split(' ')

		totalScore = self.getScore(id, self.mQuery, self.mStrQuery)

		totalScore = totalScore / len(name)	# normalizing

		return totalScore

	
	@CACHE.cache_on_arguments()
	def getScore(self, id, contentQuery, strQuery):

		idQuery = TermQuery( Term('id', id) )
		idDoc = self.mIndexSearcher.search(idQuery, 1)
		if idDoc.totalHits < 1:
			return 0.0

		doc = self.mIndexReader.document(idDoc.scoreDocs[0].doc)
		parentID = doc.get('parentID')
		
		childScore = self.mIndexSearcher.explain(contentQuery, idDoc.scoreDocs[0].doc).getValue()
		parentScore = 0.0
		if int(parentID) > 0:
			parentScore = self.getScore(parentID, contentQuery, strQuery)
		
		return childScore + parentScore
		

class CommandScoreQuery(PythonCustomScoreQuery):

	def __init__(self, mainQuery, strQuery):

		PythonCustomScoreQuery.__init__(self, mainQuery)
		
		self.mStrQuery = strQuery


	def getCustomScoreProvider(self, context):
		
		return CommandScoreProvider(context, self.mStrQuery)	
