from django.urls import path
from .views import *

urlpatterns = [
    path('url_player',Get_Url_Scraping)
]