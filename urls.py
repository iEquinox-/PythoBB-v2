from django.conf.urls import patterns, include, url
from django.contrib import admin

import Frame,Pages

urlpatterns = patterns('',
	url(r'^$', Frame.Base().Home, name='Index'),
	url(r'^login/$', Frame.Base().Login, name='Login'),
	url(r'^js/(?P<fname>\w+).js', Pages.Pages()._JS, name='JavaScript File'),
	url(r'^css/(?P<fname>\w+).css$', Pages.Pages()._CSS, name='CSS File'),
)
