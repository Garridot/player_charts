from django.contrib import admin
from .models import *
# Register your models here.

class PlayersAdmin(admin.ModelAdmin):
    list_display  = ('id','name','nationality')    
    search_fields = ('name',)


class PlayerStatAdmin(admin.ModelAdmin):
    list_display  = ('id','player','team','competition','goals','assists','games','wins','draws','defeats','team_goals','season')    
    search_fields = ('player','team','competition','season')    
    list_filter   = ('player','season','team')

admin.site.register(Player,PlayersAdmin)
admin.site.register(Player_Stats_by_Season,PlayerStatAdmin)

