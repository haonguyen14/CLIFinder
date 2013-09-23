import threading
from time import time

TIMEOUT = 2.0


class LoggingBot(threading.Thread):

	def __init__(self, message, queue, timeout = TIMEOUT):
		
		threading.Thread.__init__(self)
		self.mMessage = message

		self.mQueue = queue
		self.mTimeout = timeout
	
	def run(self):
		
		start = time()
		while not self.mQueue[1].acquire(True):
			if time() - start > self.mTimeout:
				return
			else:
				pass

		self.mQueue[0].put(self.mMessage)
		self.mQueue[1].release()
		return
