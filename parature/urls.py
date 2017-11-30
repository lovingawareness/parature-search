from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ticket/(?P<pk>\d+)/$', views.ticket_detail, name='ticket_detail'),
]
