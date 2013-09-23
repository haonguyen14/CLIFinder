import Queue
import os
import time
import threading


BUFFERING_MAX = 0
SLEEPING_INTERVAL =  2 


class LoggingEngine(threading.Thread):
	
	#Overriden
	def __init__ (self, path, name, queue):
	
		threading.Thread.__init__(self, name = name)
		self.daemon = True

		self.mRunning = True
		self.mPath = path
		self.mQueue = (queue, threading.Lock())


	#Overriden
	def run(self):	 
		fd = open(self.mPath, 'a+', BUFFERING_MAX)

		try:
			while self.mRunning and fd != None:
				self.mQueue[1].acquire()

				if not self.mQueue[0].empty():
					message = self.mQueue[0].get()
					fd.write(message)
					fd.flush()

				self.mQueue[1].release()
				time.sleep(SLEEPING_INTERVAL)
		except:
			pass
		else:
			print "%s thread stopped ..." % self.getName()
			fd.close()


	def stop(self):
		self.mRunning = False
	
