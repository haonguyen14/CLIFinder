import lucene

from org.apache.pylucene.search.similarities import PythonDefaultSimilarity


class DecreaseLengthNormSimilarity(PythonDefaultSimilarity):

	def lengthNorm(self, state):

		numTerms = state.getLength()
		if numTerms == 0:
			return 0.0		

		return 0.04 / numTerms
