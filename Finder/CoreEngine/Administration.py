import lucene
import os
import Queue
import atexit

from Custom.Similarity.DecreaseLengthNormSimilarity import DecreaseLengthNormSimilarity
from Custom.Analysis.PorterStemmingAnalyzer import PorterStemmingAnalyzer
from LoggingEngine import LoggingEngine

from java.io import File
from java.util import HashMap

from org.apache.lucene.util import Version
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.index import DirectoryReader, IndexWriterConfig
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper
from org.apache.lucene.search import IndexSearcher


####################### QueryParser Configuration #####################
PHRASE_QUERY_BY_DEFAULT		= True
PHRASE_SLOP			= 2
FUZZY_MIN_SIM			= 3.0
DEFAULT_OPERATOR		= QueryParser.Operator.OR
######################################################################


class Administration():

	def __init__ (self):
		
		self.mDocumentDirectory = "/home/hnguyen/Projects/CLIFinder/operations.sub"
		self.mIndexDirectory = "/home/hnguyen/Projects/CLIFinder/cli.index"

		self.mIndexReader = None
		if os.path.isdir(self.mIndexDirectory) and self.mIndexReader == None:
			directory = SimpleFSDirectory(File(self.mIndexDirectory))
			self.mIndexReader = DirectoryReader.open(directory)

		
		############################### IndexingEngine Settings ######################################
		self.mSimilarity = DecreaseLengthNormSimilarity()
		self.mOpenMode = IndexWriterConfig.OpenMode.CREATE
		##############################################################################################
				
		self.mIsDebug = False

		if self.mIsDebug:
		############################### Setting up loggers ###########################################
			self.mIndexingLogPath = "/home/hnguyen/Projects/CLIFinder/logs/indexing.log"
			self.mSearchingLogPath = "/home/hnguyen/Projects/CLIFinder/logs/searching.log"
	
			self.mIndexingLogger = LoggingEngine(self.mIndexingLogPath, "IndexingLogger", Queue.Queue())
			self.mSearchingLogger = LoggingEngine(self.mSearchingLogPath, "SearchingLogger", Queue.Queue())

			self.mIndexingLogger.start()
			self.mSearchingLogger.start()
			atexit.register(self.clear)
		#############################################################################################	

	

	def clear(self):
	
		print 'Clearing ... '	
		indexingLoggerLock = self.getIndexingLogQueue()[1]
		searchingLoggerLock = self.getSearchingLogQueue()[1]

		while not indexingLoggerLock.acquire(False):
			pass
		while not searchingLoggerLock.acquire(False):
			pass

		self.mIndexingLogger.stop()
		self.mSearchingLogger.stop()

		indexingLoggerLock.release()
		searchingLoggerLock.release()


	def getIndexingAnalyzers(self):
		
		return {
			'default' 	: PorterStemmingAnalyzer(Version.LUCENE_CURRENT),
			'name'		: KeywordAnalyzer(),
			'parent'	: KeywordAnalyzer(),
			'id'		: KeywordAnalyzer()	
			}

	
	def getSearchingAnalyzers(self):
		
		return {
			'default' 	: PorterStemmingAnalyzer(Version.LUCENE_CURRENT),
			'name'		: KeywordAnalyzer(),
			'parent'	: KeywordAnalyzer(),
			'id'		: KeywordAnalyzer()
			}


	def getQueryParser(self):
		
		analyzers = self.getSearchingAnalyzers()

		map = HashMap()
		map.put('name', analyzers['name'])
		map.put('parent', analyzers['parent'])
		map.put('content', analyzers['default'])
		map.put('id', analyzers['id'])
		analyzerWrapper = PerFieldAnalyzerWrapper(analyzers['default'], map)

		queryParser = QueryParser(Version.LUCENE_CURRENT, 'content', analyzerWrapper)

		queryParser.setAutoGeneratePhraseQueries(PHRASE_QUERY_BY_DEFAULT)
		queryParser.setPhraseSlop(PHRASE_SLOP)
		queryParser.setFuzzyMinSim(FUZZY_MIN_SIM)
		queryParser.setDefaultOperator(DEFAULT_OPERATOR)

		return queryParser


	def getIndexSearcher(self):

		indexSearcher = IndexSearcher(self.mIndexReader)
		if self.mSimilarity != None:
			indexSearcher.setSimilarity(self.mSimilarity)
		
		return indexSearcher	


	def getIndexingLogQueue(self):
		
		if self.mIsDebug:	
			return self.mIndexingLogger.mQueue
		return None

	def getSearchingLogQueue(self):
		if self.mIsDebug:
			return self.mSearchingLogger.mQueue
		return None
