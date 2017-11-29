from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ticket_list, name='ticket_list'),
    url(r'^ticket/(?P<pk>\d+)/$', views.ticket_detail, name='ticket_detail'),
    url(r'^search-form/$', views.search_form, name='search_form'),
    url(r'^search/$', views.search, name='search'),
]
