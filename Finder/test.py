import lucene
import sys

from Indexer import Indexer
from Searcher import Searcher
from Analyzer import Analyzer

from java.io import StringReader
from org.apache.lucene.analysis import TokenStream
from org.apache.lucene.index import IndexWriterConfig
from org.apache.lucene.util import Version
from org.apache.lucene.search import Explanation

lucene.initVM()


analyzer = Analyzer(Version.LUCENE_CURRENT)
config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

indexer = Indexer(config, '/home/hnguyen/Projects/CLIFinder/cli.index')
indexer.index('/home/hnguyen/Projects/CLIFinder/cli')

searcher = Searcher(analyzer, '/home/hnguyen/Projects/CLIFinder/cli.index')

while True:
	strQuery = raw_input("Query:")
	if strQuery == '':
		sys.exit(1)

	docs, query = searcher.search(strQuery, 'content', 'name')

	print '"%s" has %s result(s)' % (strQuery, len(docs))
	for d in docs:
		print 'Score: %s \nFile: %s \nDesc: %s \n' % (d.score, searcher.mIndexSearcher.doc(d.doc).get('name'), searcher.mIndexSearcher.doc(d.doc).get('content'))

	print "<================================================>"
