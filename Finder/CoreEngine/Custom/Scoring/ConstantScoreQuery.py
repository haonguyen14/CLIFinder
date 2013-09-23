import lucene

from org.apache.pylucene.queries import PythonCustomScoreQuery, PythonCustomScoreProvider


class ConstantScoreProvider(PythonCustomScoreProvider):

	def customScore(self, doc, subQueryScore, valSrcScore):
		
		return subQueryScore * 1;


class ConstantScoreQuery(PythonCustomScoreQuery):

	def getCustomScoreProvider(self, context):
		
		provider = ConstantScoreProvider(context)
		return provider
