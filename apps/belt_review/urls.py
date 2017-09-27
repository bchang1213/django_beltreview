from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^books$', views.loggedin),
	url(r'^books/(?P<book_id>\d+)$', views.specificbook, name = 'specificbook'),
	url(r'^books/add$', views.bookform),
	url(r'^submit$', views.submit),
	url(r'^reviewsubmit$', views.reviewsubmit),
	url(r'^users/(?P<user_id>\d+)$', views.users),
	url(r'^books/(?P<book_id>\d+)/(?P<review_id>\d+)/delete$', views.delete),
	#(?P<user_id>\d+)
  ]