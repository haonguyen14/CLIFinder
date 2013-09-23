from dogpile.cache.proxy import ProxyBackend
import Queue


def key_generator(namespace, fn):
	
	def generator(*args):
		return (fn.__name__, args[1], args[3])
	return generator

class MemoryBackendProxy(ProxyBackend):

	def __init__(self):
		ProxyBackend.__init__(self)
		self.queue = Queue.Queue()


	def set(self, key, value):

		if self.queue.qsize() > 10000:
			item = self.queue.get()
			self.proxied.delete(item[0])

		self.queue.put( (key, value) )
		self.proxied.set(key, value)


	def get(self, key):
		return self.proxied.get(key)
