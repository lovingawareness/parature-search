from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/tickets/', views.ticket_search, name='ticket_search'),
    url(r'^search/customers/', views.customer_search, name='customer_search'),
    url(r'^search/comment_search_by_csr/', views.comment_search_by_csr, name='comment_search_by_csr'),
    url(r'^ticket/(?P<pk>\d+)/$', views.ticket_detail, name='ticket_detail'),
    url(r'^customer/(?P<pk>\d+)/$', views.customer_detail, name='customer_detail'),
    url(r'^comment/(?P<pk>\d+)/$', views.comment_detail, name='comment_detail'),
]
