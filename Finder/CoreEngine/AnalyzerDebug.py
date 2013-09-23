import lucene

from java.io import StringReader

from org.apache.lucene.analysis.tokenattributes import CharTermAttributeImpl


class AnalyzerDebug:

	
	@classmethod
	def debug(cls, analyzer, str):

		tokenStream = analyzer.tokenStream('debug', StringReader(str))
		termAttr = tokenStream.addAttribute(lucene.findClass('org/apache/lucene/analysis/tokenattributes/CharTermAttribute'))
		
		str = ''
		tokenStream.reset()
		while tokenStream.incrementToken():
			
			str = str + ('[%s] ' % termAttr.toString())

		return str
