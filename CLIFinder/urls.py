from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^tools/indexing', 'Finder.views.indexing'),
	url(r'^logs/indexing', 'Finder.views.indexingLog'),
	url(r'^logs/searching', 'Finder.views.searchingLog'),
	url(r'^/*', 'Finder.views.index'),
)
