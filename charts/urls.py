from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('search',search_players,name='search_players'),
    path('players',players,name='players'),
    path('<str:player>',get_stats,name='get_stats'),
    path('general_stats/<str:player>/<str:team>',general_stats,name='general_stats'),    
    path('goals_involvements_season/<str:player>/<str:team>',goals_involvements_season,name='goals_involvements_season'), 
    path('goal_involvements_rate/<str:player>/<str:team>',goal_involvements_rate,name='goal_involvements_rate'),
    path('performance_competition/<str:player>/<str:team>',performance_competition,name='performance_competition'),    
    path('goals_involvements_rate/<str:player>/<str:team>',goals_involvements_rate,name='goals_involvements_rate'), 
    path('career_games/<str:player>/<str:team>',career_games,name="career_games"),
    
    path('players_comparison/',comparison_form,name='comparison_form'),
    path('player_comparison/general_stats/<str:first_player>/<str:second_player>',comparison_stats,name='comparison_stats'),
    path('player_comparison/byseason/<str:first_player>/<str:second_player>',comparation_bySeason), 
    path('player_comparison/bycompetition/<str:first_player>/<str:second_player>',comparation_byCompetition),
]
