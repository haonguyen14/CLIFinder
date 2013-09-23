from Finder.models import Result, Command
import os
import time

from CoreEngine.IndexingEngine import IndexingEngine
from CoreEngine.SearchingEngine import SearchingEngine

from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.servers.basehttp import FileWrapper


import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.util import Version
from org.apache.lucene.search import Explanation

INDEX_DIRECTORY = "/home/hnguyen/Projects/CLIFinder/cli.index"


def index(request):

	results = []

	initTime = time.time()
	if 'search' in request.REQUEST and request.REQUEST['search'] != '':
		jvm = settings.JAVAVM
		jvm.attachCurrentThread()
	
		searchingEngine = SearchingEngine()
		docs = searchingEngine.searching(request.REQUEST['search'])
		for d in docs:
			results.append(Result(d['name'], d['parent'], d['content'], d['score']))

	timeInt = time.time() - initTime
	template = loader.get_template('index.html')
	context = RequestContext(request, {'request': request, 'len': len(results), 'results': results, 'time': "%.3f" % timeInt})

	return HttpResponse(template.render(context))


def indexing(request):

	jvm = settings.JAVAVM
	jvm.attachCurrentThread()
	indexingEngine = IndexingEngine()
	indexingEngine.indexing()

	return index(request)


def indexingLog(request):

	fd = open(settings.ADMINS_ENGINE.mIndexingLogPath, 'r')
	wrapper = FileWrapper(fd)

	response = HttpResponse(wrapper, content_type="text/plain")
	response['Content-Length'] = os.path.getsize(settings.ADMINS_ENGINE.mIndexingLogPath)
	return response


def searchingLog(request):

	fd = open(settings.ADMINS_ENGINE.mSearchingLogPath, 'r')
	wrapper = FileWrapper(fd)
	
	response = HttpResponse(wrapper, content_type="text/plain")
	response['Content-Length'] = os.path.getsize(settings.ADMINS_ENGINE.mSearchingLogPath)
	return response
