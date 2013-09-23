import lucene

from java.io import StringReader

from org.apache.lucene.analysis.tokenattributes import CharTermAttributeImpl


class KeywordExtractor:

	def __init__ (self):
		
		return
	

	def extract(self, analyzer, str):

		tokenStream = analyzer.tokenStream('content', StringReader(str))
		termAttr = tokenStream.addAttribute(lucene.findClass('org/apache/lucene/analysis/tokenattributes/CharTermAttribute'))
		
		keywords = []
		tokenStream.reset()
		while tokenStream.incrementToken():
			
			keywords.append(termAttr.toString())

		return keywords
