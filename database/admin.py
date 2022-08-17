from django.contrib import admin
from .models import *
# Register your models here.

class PlayersAdmin(admin.ModelAdmin):
    list_display  = ('id','name','nationality')    
    search_fields = ('name',)
    

class PlayerTeamStatsAdmin(admin.ModelAdmin):
    list_display  = ('id','player','team','competition','games','goals','assists','season')    
    search_fields = ('player','team','competition','season')    
    list_filter   = ('player','season','team')


class MatchesAdmin(admin.ModelAdmin):
    list_display  = ('id','player','team','date','competition','home_team','result','goals','away_team','assists','season')    
    search_fields = ('player','team','competition','season')    
    list_filter   = ('player','season','team')

admin.site.register(Player,PlayersAdmin)
admin.site.register(Player_Team_Stats,PlayerTeamStatsAdmin)
admin.site.register(Player_Matches,MatchesAdmin)


