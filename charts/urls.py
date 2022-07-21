from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('<str:player>',get_stats,name='get_stats'),
    path('general_stats/<str:player>/<str:team>',general_stats,name='general_stats'),    
    path('gls_as_season/<str:player>/<str:team>',gls_as_season,name='gls_as_season'), 
    path('goal_involvements/<str:player>/<str:team>',goal_involvements,name='goal_involvements'),
    path('performance_competition/<str:player>/<str:team>',performance_competition,name='performance_competition'),
    
]
