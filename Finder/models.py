import os

from django.db import models


#################
# Search Result #
#################

class Result:
	
	def __init__(self, name, parent, content, score):
		self.mName = name
		self.mParent = parent
		self.mContent = content
		self.mScore = score



#################
# Command Model #
#################

class Command:
	
	def __init__ (self, name, parent, desc):
	
		self.mName = name
		self.mParent = parent
		self.mDesc = desc

		self.mFullPath = ""
			
		
	def getFullPath(self):

		if self.mParent == None:	
			return self.mName

		return self.mParent.getFullPath() + " " + self.mName



	def getParentFromPath(self, path):
		return None	
