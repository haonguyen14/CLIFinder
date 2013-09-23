import datetime
import lucene

from Custom.Scoring.CommandScoreQuery import CommandScoreQuery
from Custom.Scoring.ConstantScoreQuery import ConstantScoreQuery
from AnalyzerDebug import AnalyzerDebug
from LoggingBot import LoggingBot

#import settings
from django.conf import settings


from org.apache.lucene.util import Version
from org.apache.lucene.search import TermQuery, BooleanQuery, BooleanClause


IS_DEBUG = settings.ADMINS_ENGINE.mIsDebug


class SearchingEngine:

	def __init__ (self):

		self.mIndexSearcher = settings.ADMINS_ENGINE.getIndexSearcher()		
		self.mQueryParser = settings.ADMINS_ENGINE.getQueryParser()	
		self.mLog = ''
	

	def searching (self, strQuery):

		query = self.mQueryParser.parse(strQuery)
		################# testing new scorer ####################
		#testScorer = ConstantScoreQuery(query)
		testScorer = CommandScoreQuery(query, strQuery)
		#########################################################

		
		topDocs = self.mIndexSearcher.search(testScorer, 10)
		scoreDocs = topDocs.scoreDocs		

		ret = []
		for d in scoreDocs:
			doc = self.mIndexSearcher.doc(d.doc)
		
			name = doc.get('name')
			parent = doc.get('parent')
			content = doc.get('content')

			ret.append({
				'name' 		: name,
				'parent' 	: parent,
				'content'	: content,
				'score'		: d.score,
			})
		
		################# Debug Query Analyzer ############
		if IS_DEBUG:
			self.mLog = self.mLog + ("%s - %s\n" % (datetime.datetime.now(), strQuery))
			self.mLog = self.mLog + ("   Parsed Query: <%s>\n" % query.toString())
			self.mLog = self.mLog + ("   Hits: %s\n   MaxScore: %s\n" % (topDocs.totalHits, topDocs.getMaxScore()) )
			self.mLog = self.mLog + ("   Scorer: %s\n\n" % testScorer )			


			loggingBot = LoggingBot(self.mLog, settings.ADMINS_ENGINE.getSearchingLogQueue())
			loggingBot.start()
			self.mLog = ""
		
		return ret
