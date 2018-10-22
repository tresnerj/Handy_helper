from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^dashboard$', views.index),
    url(r'^logout$', views.logout),
    url(r'^addJob$', views.addJob),
    url(r'^add$', views.add),
    url(r'^view/(?P<id>\d+)$', views.view),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^processedit/(?P<id>\d+)$', views.processEdit),
    url(r'^getJob/(?P<id>\d+)$', views.getJob),
    url(r'^done/(?P<id>\d+)$', views.done),
]