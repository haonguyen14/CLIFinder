import os
import lucene

from LoggingBot import LoggingBot
from AnalyzerDebug import AnalyzerDebug

from django.conf import settings
#import settings

from java.io import File
from java.util import HashMap

from org.apache.lucene.util import Version
from org.apache.lucene.analysis.miscellaneous import PerFieldAnalyzerWrapper
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, FieldType


IS_DEBUG = settings.ADMINS_ENGINE.mIsDebug


class IndexingEngine():

	def __init__(self):

		self.mDocumentDirectory = settings.ADMINS_ENGINE.mDocumentDirectory
		self.mIndexDirectory = settings.ADMINS_ENGINE.mIndexDirectory
		self.mAnalyzers = settings.ADMINS_ENGINE.getIndexingAnalyzers()


		############################# Writer Configurattion #####################################
		map = HashMap()
		map.put('name', self.mAnalyzers['name'])
		map.put('parent', self.mAnalyzers['parent'])
		map.put('content', self.mAnalyzers['default'])
		map.put('id', self.mAnalyzers['id'])		

		analyzerWrapper = PerFieldAnalyzerWrapper(self.mAnalyzers['default'], map)

		self.mWriterConfig = IndexWriterConfig(Version.LUCENE_CURRENT, analyzerWrapper)
		self.mWriterConfig.setOpenMode(settings.ADMINS_ENGINE.mOpenMode)

		if settings.ADMINS_ENGINE.mSimilarity != None:
			self.mWriterConfig.setSimilarity(settings.ADMINS_ENGINE.mSimilarity)
		########################################################################################


		directory = SimpleFSDirectory(File(self.mIndexDirectory))
		self.mIndexWriter = IndexWriter(directory, self.mWriterConfig)


		############################# FieldType Prepration #####################
		nameField = FieldType()
		nameField.setIndexed(True)
		nameField.setStored(True)
		nameField.setTokenized(True)
		nameField.setIndexOptions(FieldInfo.IndexOptions.DOCS_ONLY)

		parentField = FieldType()
		parentField.setIndexed(True)
		parentField.setStored(True)
		parentField.setTokenized(True)
		parentField.setIndexOptions(FieldInfo.IndexOptions.DOCS_ONLY)

		contentField = FieldType()
		contentField.setIndexed(True)
		contentField.setStored(True)
		contentField.setTokenized(True)
		contentField.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)

		idField = FieldType()
		idField.setIndexed(True)
		idField.setStored(True)
		idField.setTokenized(False)
		idField.setIndexOptions(FieldInfo.IndexOptions.DOCS_ONLY)


		self.mFieldTypes = {
			'name' 		: nameField,
			'parent'	: parentField,
			'content'	: contentField,
			'id'		: idField
		}
		#######################################################################

		self.mLog = ""

	

	def indexing(self, root = settings.ADMINS_ENGINE.mDocumentDirectory, parent = [], docID = 1, parentID = 0, id = 0):

		realPath = os.path.abspath(root)
		for i in os.listdir(realPath):

			path = os.path.join(realPath, i)
			if os.path.isfile(path):
				#index this file
				doc = Document()

				doc.add(Field('name', ("%s %s" % (' '.join(parent), i)).strip(), self.mFieldTypes['name']))
				doc.add(Field('parent', ' '.join(parent), self.mFieldTypes['parent']))
				doc.add(Field('id', str(docID), self.mFieldTypes['id']))
				doc.add(Field('parentID', str(parentID), self.mFieldTypes['id']))

				fd = open(path, 'r')
				content = fd.read()
				fd.close()

				if len(content) > 0:
					doc.add(Field('content', content, self.mFieldTypes['content']))

				self.mIndexWriter.addDocument(doc)
				##################### Logging ##############################
				if IS_DEBUG:
					nameDebug = AnalyzerDebug.debug(self.mAnalyzers['name'], ("%s %s" % (' '.join(parent), i)).strip())
					parentDebug = AnalyzerDebug.debug(self.mAnalyzers['parent'], ' '.join(parent))
					contentDebug = AnalyzerDebug.debug(self.mAnalyzers['default'], content)
					self.mLog = self.mLog + ( "File %s\n   {name - %s}: %s\n   {parent - %s}: %s\n   {content}: %s\n\n" % (path, docID, nameDebug, parentID, parentDebug, contentDebug) )



				docID = docID + 1
				################### index sub commands	
				if os.path.isdir(path + ".sub"):
					parent.append(i)
					docID = self.indexing(path + ".sub", parent, docID, docID - 1, id + 1)
					parent.pop()
					
						
		
		if id == 0:
			self.mIndexWriter.commit()
			self.mIndexWriter.close()
			
			if IS_DEBUG:
				loggingBot = LoggingBot(self.mLog, settings.ADMINS_ENGINE.getIndexingLogQueue())
				loggingBot.start()
				self.mLog = ""
		return docID

