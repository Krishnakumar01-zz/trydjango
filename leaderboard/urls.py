from django.conf.urls import include, url
from . import views
urlpatterns=[
	url(r'^$',views.home,name='home'),
	url(r'^board/(?P<pk>\d+)/$',views.link,name='link'),
	url(r'^board/new/$',views.create,name='create'),
	url(r'^form/(?P<pk>\d+)/edit/$',views.edit,name='edit'),
	url(r'^board/(?P<pk>\d+)/delete/$',views.delete,name='delete'),
	url(r'^form/signup/$',views.signup, name='signup'),
	url(r'^form/signin/$',views.signin, name='signin'),
	url(r'^form/signout/$',views.signout, name='signout')
	]