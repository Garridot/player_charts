from django.urls import path
from .views import *

urlpatterns = [
    path('url_player',get_url_scraping)
]