from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('search',search_players,name='search_players'),
    path('<str:player>',get_stats,name='get_stats'),
    path('general_stats/<str:player>/<str:team>',general_stats,name='general_stats'),    
    path('goals_involvements_season/<str:player>/<str:team>',goals_involvements_season,name='goals_involvements_season'), 
    path('goal_involvements_rate/<str:player>/<str:team>',goal_involvements_rate,name='goal_involvements_rate'),
    path('performance_competition/<str:player>/<str:team>',performance_competition,name='performance_competition'),    
    path('goals_involvements_overall_rate/<str:player>/<str:team>',goals_involvements_overall_rate,name='goals_involvements_overall_rate'), 
]
