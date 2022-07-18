from django.contrib import admin
from .models import *
# Register your models here.

class PlayersAdmin(admin.ModelAdmin):
    list_display  = ('id','name','nationality')    
    search_fields = ('name',)
    

class PlayerTeamStatsAdmin(admin.ModelAdmin):
    list_display  = ('id','player','team','competition','games','goals','assists','season')    
    search_fields = ('player','team','competition','season')    
# list_filter   = ('player','season')

admin.site.register(Player,PlayersAdmin)
admin.site.register(Player_Team_Stats,PlayerTeamStatsAdmin)

