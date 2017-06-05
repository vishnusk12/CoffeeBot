from django.conf.urls import url, include
from django.contrib import admin
from .views import Bot
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bot/Response', Bot, 'Bot')

urlpatterns = [url(r'^', include(router.urls)), ]