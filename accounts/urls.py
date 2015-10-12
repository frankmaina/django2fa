from django.conf.urls import patterns, include, url

from accounts import views

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'accounts.views.signup'),
    url(r'^signin/', 'accounts.views.signin', name='signin'),
	url(r'^signup', 'accounts.views.signup', name='signup'),
	url(r'^signout', 'accounts.views.signout_view', name='signout'),
    
)
