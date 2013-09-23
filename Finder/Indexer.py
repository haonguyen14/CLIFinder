import os
import sys
import lucene

from java.io import File
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import IndexWriter, FieldInfo
from org.apache.lucene.store import SimpleFSDirectory



class Indexer:
	
	def __init__(self, writerConfig, indexDir):
		
		lucene.initVM()

		self.mIndexDir = SimpleFSDirectory(File(indexDir))
		self.mConfig = writerConfig
		self.mWriter = IndexWriter(self.mIndexDir, self.mConfig)
	

	def index(self, root):

		t = FieldType()
		t.setIndexed(True)
		t.setStored(True)
		t.setTokenized(True)
		t.setStoreTermVectors(True)
		
		for path, dirs, files in os.walk(root):
			
			for file in files:
				
				filePath = os.path.join(path, file)
				fd = open(filePath)
				content = unicode(fd.read(), 'iso-8859-1')
				fd.close()
				
				doc = Document()
				doc.add(Field('name', file, StringField.TYPE_STORED))

				parent = os.path.split(path)[1]
				doc.add(Field('parent', parent, StringField.TYPE_STORED))

				if len(content) > 0:
					doc.add(Field('content', content, t))

				print 'Indexing %s' % file
				self.mWriter.addDocument(doc)

		self.mWriter.commit()
		self.mWriter.close()
		
		
		
		
