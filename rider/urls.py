from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^/rider/(?P<rider_id>\W+)/$', views.rider_details, name='rider_details'),
    ]