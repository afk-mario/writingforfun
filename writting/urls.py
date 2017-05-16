from django.conf.urls import url, include

from .models import Post
from .views import *

urlpatterns = [
    url(r'^$', EntryListView.as_view(), name='article-list'),
    url(r'^(?P<slug>[-\w]+)/$', EntryDetailView.as_view(), name='article-detail'),
    url(r'^post/(?P<slug>[-\w]+)$', view_post, name='post_detail'),
    url(r'^add/post$', add_post, name='add_post'),
]
