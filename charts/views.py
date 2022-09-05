from multiprocessing import context
from optparse import Values
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import render

from web_scraping.views import *
from database.models import *
import pandas as pd

from django.db.models import Q


# Create your views here.

def home(request):
    context = {}
    context['Players'] = Player.objects.all()        
    return render(request,'home.html',context)

def players(request):
    players = Player.objects.all()
    context = {'players':players}
    return render(request,'players.html',context)


def search_players(request):
    if request.method == 'POST':
        search   = str(request.POST['players']).title()
        players  = Player.objects.filter(Q(name__contains=search))
        
        context  = {'search':search,'players':players}


        return render(request,'search_result.html',context)


def get_stats(request,player):
    player = Player.objects.get(name=player)

    df = pd.DataFrame(Player_Stats_by_Season.objects.all().values()) 
    df = df[df['player_id'] == player.id]

    context = {}
    context['path']   = request.path    
    context['teams']  = df['team'].unique()
    context['player'] = player 
    return render(request,'stats.html',context)

@api_view(['GET', 'POST'])
def general_stats(request,player,team):

    player = Player.objects.get(name=player)

    context = {}
    context['Goals']     = 0
    context['Assists']   = 0
    context['Matches']   = 0    
    
    if team == 'total':
        stats = Player_Stats_by_Season.objects.filter(player=player)
    else:  
        stats = Player_Stats_by_Season.objects.filter(player=player,team=team)  

    for i in stats: context['Goals']   += i.goals 
    for i in stats: context['Assists'] += i.assists 
    for i in stats: context['Matches'] += i.games 

    context['Ratio_gls'] = round(context['Goals'] / context['Matches'],2) 
    context['Ratio_ass'] = round(context['Assists'] / context['Matches'],2)   

    total      = context['Goals'] + context['Assists'] 
    team_goals = 0
    for i in stats: team_goals   += i.team_goals
    # calculate the goals involvements %
    context['rate_involvement'] = round(total * 100 / team_goals,2)

    return Response(context)



@api_view(['GET', 'POST'])
def goals_involvements_season(request,player,team):

    # return all player's goals, player's assists, player's goals involvements and all team's goals by season  
        
    player = Player.objects.get(name=player)
    
    if team == 'total':
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player).values())
    else:  
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player,team=team).values())        

    # group by season all stats
    df = stats.groupby(['season']).sum()    

    context = {}     
        
    context['Goals']   = df['goals'].values.tolist()
    context['Assists'] = df['assists'].values.tolist()    
    context['Seasons'] = df.index.tolist()
    context['Games']   = df['games'].values.tolist() 
    
    # get goals involvements by season
    goals_involvements = []    
    for i,b in zip (context['Goals'],context['Assists']): goals_involvements.append(i+b)    
    context['goals_involvements'] =  goals_involvements
    
    return Response(context)        


@api_view(['GET', 'POST'])
def goal_involvements_rate(request,player,team):

    # return the rate of goals involvements by season  
      
    player = Player.objects.get(name=player)     
    
    if team == 'total':
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player).values())
    else:  
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player,team=team).values())    
    
    
    # group by season all matches
    df = stats.groupby(['season']).sum()

    context = {}    
     
    Goals    = df['goals'].values.tolist()
    Assists  = df['assists'].values.tolist()
    Total_gf = df['team_goals'].values.tolist()    

    involvements = []
    for g,a,t in zip(Goals,Assists,Total_gf): 

        # if 'Total_gf' is equal to 0, replace to 1(You can not divide by zero)                  
        try:    involvements.append( round(( (g + a) * 100) / t , 2))
        except: involvements.append( round(( (g + a) * 100) / 1 , 2))   

    context['Seasons']      = df.index.tolist()
    context['Goal_Involvements_Rate'] = involvements

    return Response(context)   


@api_view(['GET', 'POST'])
def performance_competition(request,player,team):

    # return all player's goals, player's assists, player's goals involvements and player's matches by competition
    
    player = Player.objects.get(name=player)     
    
    if team == 'total':
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player).values())
    else:  
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player,team=team).values()) 

    df = stats.groupby(['competition']).sum()

    context = {}     

    goals    = df['goals'].values.tolist()
    assists  = df['assists'].values.tolist()
    team_gls = df['team_goals'].values.tolist()
    
    performance = []
    for g,a,t in zip(goals,assists,team_gls): 
        # if 'team_gls' is equal to 0, replace to 1(You can not divide by zero)  
        try:    performance.append(round(((g+a)*100) / int(t),2))
        except: performance.append(round(((g+a)*100) / 1,2))

    df['performance'] = performance 

    context['Competition'] = df.index.unique().to_list()    
    context['games']       = df['games'].values.tolist() 
    context['goals']       = df['goals'].values.tolist()
    context['assists']     = df['assists'].values.tolist() 
    context['performance'] = df['performance'].values.tolist() 
    
    return Response(context)   


@api_view(['GET', 'POST'])
def goals_involvements_overall_rate(request,player,team):

    player = Player.objects.get(name=player)     
    
    if team == 'total':
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player).values())
    else:  
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player,team=team).values())

    context = {}

    context["team_goals"]   = stats['team_goals'].sum()
    context["player_goals"] = stats['goals'].sum()
    context["player_assists"] = stats['assists'].sum()
    context["rate_goals_involvements"]  = round((stats['goals'].sum() + stats['assists'].sum()) * 100 / stats['team_goals'].sum(),2)

    return Response(context)     

    
