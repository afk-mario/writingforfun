from django.conf.urls import url, include

from .models import Post
from .views import *

urlpatterns = [
    url(r'^post/(?P<slug>[-\w]+)$', 
        view_post,
        name='writting_post_detail'),
    url(r'^add/post$', 
        add_post, 
        name='writting_add_post'),
]
