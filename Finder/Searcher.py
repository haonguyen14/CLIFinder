import lucene

from Indexer import Indexer

from java.io import File

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index  import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.util import Version


class Searcher:
	
	def __init__(self, analyzer, indexDir):
	
		self.mAnalyzer = analyzer
		
		dir = SimpleFSDirectory(File(indexDir))
		self.mIndexSearcher = IndexSearcher(DirectoryReader.open(dir))


	def search(self, strQuery, fieldName, fieldName_2):
		
		query = QueryParser(Version.LUCENE_CURRENT, fieldName, self.mAnalyzer).parse(strQuery)
		docs  = self.mIndexSearcher.search(query, 50).scoreDocs

		if len(docs) < 1:
			query = QueryParser(Version.LUCENE_CURRENT, fieldName_2, StandardAnalyzer(Version.LUCENE_CURRENT)).parse(strQuery)
			docs = self.mIndexSearcher.search(query, 50).scoreDocs

		return docs, query
		
