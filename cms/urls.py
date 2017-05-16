from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from .models import Post
from .views import *

urlpatterns = [
    # url(r'^test/$', test_mail, name='mail'),
    url(r'^register/$', Register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    url(r'^(?P<slug>[-\w]+)/$', EntryDetailView.as_view(), name='article-detail'),
    url(r'^post/(?P<slug>[-\w]+)$', view_post, name='post_detail'),
    url(r'^add/post$', add_post, name='add_post'),

    url(r'^$', EntryListView.as_view(), name='home'),
]
