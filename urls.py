from django.conf.urls import patterns, include, url
from django.contrib import admin

import Frame,Pages,Settings,API,Misc

urlpatterns = patterns('',
	url(r'^$', Frame.Base().Home, name='Index'),
	url(r'^login/$', Frame.Base().Login, name='Login'),
	url(r'^login/_login/$', Frame.Base().ProcessLogin, name='Login'),
	url(r'^register/$', Frame.Base().Register, name='Register'),
	url(r'^register/_register/$', Frame.Base().ProcessRegister, name='Register'),
	url(r'^member/profile/(?P<uid>\d+)/$', Frame.Base().MakeProfile, name='Profile'),
	url(r'^member/usercp/$', Frame.Base().ControlPanel, name='User CP'),
	url(r'^member/usercp/_usercp/$', Frame.Base().ProcessUserCP, name='User CP'),
	url(r'^search/$', Misc.Search().doSearch, name='Search'),
	url(r'^forum/(?P<fid>\d+)/$', Frame.Base().Forum, name='Forum'),
	url(r'^thread/(?P<tid>\d+)/$', Frame.Base().Thread, name='Thread'),
	url(r'^action/$', Misc.Actions().Action, name='Action'),
	url(r'^js/(?P<fname>\w+).js', Pages.Pages()._JS, name='JavaScript File'),
	url(r'^css/(?P<fname>\w+).css$', Pages.Pages()._CSS, name='CSS File'),
	url(r'^api/v1/(?P<type>\w+)/(?P<requested>\w+|\*)/$', API.API().RenderJSON, name='API')
)
