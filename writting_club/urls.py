from django.conf.urls import url, include
from django.contrib.auth import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^accounts/login/$', views.auth_login),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^writting/', include('writting.urls')),
]
