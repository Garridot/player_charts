from multiprocessing import context
from os import stat
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import render

from web_scraping.views import *
from database.models import *
import pandas as pd

from .utils import * 

from django.db.models import Q


# Create your views here.

def home(request):
    context = {}
    context['players'] = Player.objects.all()[:9]        
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
    context['teams']  = df['team'].unique()
    context['player'] = player 
    return render(request,'stats.html',context)



@api_view(['GET', 'POST'])
def general_stats(request,player,team):

    player = Player.objects.get(name=player)

    context = {}
    context['player']    = player.name
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

    # total      = context['Goals'] + context['Assists'] 
    # team_goals = 0
    # for i in stats: team_goals   += i.team_goals
    # # calculate the goals involvements %
    # context['rate_involvement'] = round(total * 100 / team_goals,2)

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

    df.sort_values(by=['games'], inplace=True, ascending=False)

    context['Competition'] = df.index.unique().to_list()    
    context['games']       = df['games'].values.tolist() 
    context['team_goals']  = df['team_goals'].values.tolist()
    context['goals']       = df['goals'].values.tolist()
    context['assists']     = df['assists'].values.tolist() 
    context['performance'] = df['performance'].values.tolist() 
    
    return Response(context)   


@api_view(['GET', 'POST'])
def goals_involvements_rate(request,player,team):

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



@api_view(['GET', 'POST'])
def career_games(request,player,team):

    player = Player.objects.get(name=player)     

    if team == 'total':
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player).values())
    else:  
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player,team=team).values())

    context = {}
    context['games']  = stats['games'].sum()
    context['wins']   = stats['wins'].sum()
    context['draws']  = stats['draws'].sum()
    context['defeats']  = stats['defeats'].sum()   

    return Response(context)  



import json

def international_competition():
    player = Player.objects.get(name="Neymar")

    team = "total" 

    if team == 'total':
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player).values())

        
    else:  
        stats = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player,team=team).values())     

    

    # Club league Competition
    filter_league = ["LaLiga","Ligue 1","Serie A","Premier League","Bundesliga","Eredivisie"]    

    club_league = stats.loc[stats['competition'].str.contains('|'.join(filter_league))]
    club_league = club_league.groupby(['competition']).sum()



    uefa_league = stats.loc[stats['competition'].str.contains('|'.join(['UEFA Champions League',"Europa League"]))]

    # remove qualifying rows
    uefa_league = uefa_league.loc[uefa_league['competition'].str.contains("Qualifying") == False]


    uefa_league = uefa_league.groupby(['competition']).sum()   


    
   

    
    

    
    





    # Nation Competition
    nation = stats.loc[stats['competition'].str.contains('|'.join(['Copa América',"EURO","World Cup"]))] 
    nation['competition'] = nation['competition'].str.replace('\d+', '')

    # remove qualifying or world cup club row
    nation = nation.loc[nation['competition'].str.contains('|'.join(["qualification","FIFA Club"])) == False]

    nation['competition'] = nation['competition'].str.strip()
    nation = nation.groupby(['competition']).sum()

    print(nation)


    # if "World Cup" in nation.index:
    #     world_cup = nation.loc[nation.index.str.len() == 9]
    # else: world_cup = 0

    # if "EURO" in nation.index:        
    #     continental = nation.loc[nation.index.str.len() == 4]
    # elif "Copa América" in nation.index:
    #     continental = nation.loc[nation.index.str.len() == 12]
    # else:
    #     continental = 0   
    
    
    # result = pd.DataFrame({'bla':[1,2,3],'bla2':['a','b','c']}).to_json(orient='records')
    # print(json.loads(result))


    

    

      
   

     
# international_competition()     













#### PLAYERS COMPARATION #### 

    
def player_comparison(request):
    players = Player.objects.all()
    context = {}
    context['players'] = players

    if request.method == 'POST':
        first_player  = Player.objects.get(name=request.POST['first_player'])
        second_player = Player.objects.get(name=request.POST['second_player'])
        context['first_player']  = first_player
        context['second_player'] = second_player       
        return render(request,'player_comparison.html',context)

    return render(request,'player_comparison.html',context)



@api_view(['GET', 'POST'])
def goal_involvements_players(request,first_player,second_player):

    # return the rate of goals involvements by season  
      
    player_1 = Player.objects.get(name=first_player) 
    player_2 = Player.objects.get(name=second_player)

    df  = pd.DataFrame(Player_Stats_by_Season.objects.filter(player__in=[player_1,player_2]).values())    

    df_p1 = df[df['player_id'] == player_1.id]
    df_p2 = df[df['player_id'] == player_2.id]

    stats_1  = get_goal_involvements_rate(df_p1)
    stats_2  = get_goal_involvements_rate(df_p2)

    stats_1['goal_involvements_rate_player1'] = stats_1.pop('goal_involvements_rate')
    stats_2['goal_involvements_rate_player2'] = stats_2.pop('goal_involvements_rate')

    stats = pd.DataFrame(stats_1).append(pd.DataFrame(stats_2),ignore_index=True).groupby(['seasons']).sum() 

    context = {}
    context['seasons'] = stats.index.tolist()
    context['player1'] = player_1.name   
    context['player2'] = player_2.name 
    context['goal_involvements_rate_player1'] = stats['goal_involvements_rate_player1']
    context['goal_involvements_rate_player2'] = stats['goal_involvements_rate_player2']

    return Response(context)  
    

    print(stats)



@api_view(['GET', 'POST'])
def performance_competition_players(request,first_player,second_player):

    player_1 = Player.objects.get(name=first_player) 
    player_2 = Player.objects.get(name=second_player)

    df1  = pd.DataFrame(Player_Stats_by_Season.objects.filter(player__in=[player_1]).values()) 
    df2  = pd.DataFrame(Player_Stats_by_Season.objects.filter(player=player_2,competition__in=df1['competition'].unique().tolist()).values())

    df_1 = df1[['competition', 'goals',  'assists',  'games']]    
    dict_1 = {'competition':'competition','goals':'goals_player1','assists':'assists_player1','games':'games_player1'}
    df_1.rename(columns=dict_1,inplace=True)    
    
    df_2 = df2[['competition', 'goals',  'assists',  'games']]
    dict_2 = {'competition':'competition','goals':'goals_player2','assists':'assists_player2','games':'games_player2'}
    df_2.rename(columns=dict_2,inplace=True)

    df = df_1.append(df_2).groupby(['competition']).sum()
    
    df = df.loc[(df['games_player1'] != 0) & (df['games_player2'] != 0)]

    
    
    dic_player_1 = {}

    dic_player_1['competitions'] = df.index.unique().to_list() 
    dic_player_1['games']        = df['games_player1'].values.tolist() 
    dic_player_1['goals']        = df['goals_player1'].values.tolist() 
    dic_player_1['assists']      = df['assists_player1'].values.tolist()
    dic_player_1['name']         = player_1.name 

    dic_player_2 = {}

    dic_player_2['competitions'] = df.index.unique().to_list() 
    dic_player_2['games']       = df['games_player2'].values.tolist() 
    dic_player_2['goals']       = df['goals_player2'].values.tolist() 
    dic_player_2['assists']     = df['assists_player2'].values.tolist() 
    dic_player_2['name']         = player_2.name 

    return Response({'player_1': dic_player_1,'player_2':dic_player_2})    


@api_view(['GET', 'POST'])
def goals_by_age(request,first_player,second_player):

    player_1 = Player.objects.get(name=first_player) 
    player_2 = Player.objects.get(name=second_player)

    df1 = pd.DataFrame(Player_Stats_by_Season.objects.filter(player__in=[player_1]).values())
    df2 = pd.DataFrame(Player_Stats_by_Season.objects.filter(player__in=[player_2]).values())  
    
    ages_p1 = get_ages(df1,player_1.age)
    ages_p2 = get_ages(df2,player_2.age)  


    goals_p1 = []
    goals_p2 = []

    goals  = 0
    goals2 = 0

    for i in df1.groupby(['season']).sum()['goals']: 
        goals += i
        goals_p1.append(goals)

    for i in df2.groupby(['season']).sum()['goals']: 
        goals2 += i
        goals_p2.append(goals2)

    dic_player1 = {'goals_p1':goals_p1,'age':ages_p1[::-1]} 
    dic_player2 = {'goals_p2':goals_p2,'age':ages_p2[::-1]}     

    df = pd.DataFrame(dic_player1)
    df = df.append(pd.DataFrame(dic_player2)).groupby(['age']).sum()

    
    context = {}
    context['ages']     = df.index.tolist()
    context['p1']       = player_1.name 
    context['goals_p1'] = df['goals_p1']
    context['p2']       = player_2.name 
    context['goals_p2'] = df['goals_p2']

    return Response(context)


  

    

    



   


    

   


    



