from django.views.generic import RedirectView
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='search/')),
    url(r'^search/', views.ticket_search, name='ticket_search'),
    url(r'^ticket/(?P<pk>\d+)/$', views.ticket_detail, name='ticket_detail'),
    url(r'^customer/(?P<pk>\d+)/$', views.customer_detail, name='customer_detail'),
    url(r'^comment/(?P<pk>\d+)/$', views.comment_detail, name='comment_detail'),
]
