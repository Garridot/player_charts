from django.shortcuts import render
from django.http import JsonResponse
from web_scraping.views import *
from database.models import *
import pandas as pd


# Create your views here.

def home(request):
    context = {}
    context['Players'] = Player.objects.all()        
    return render(request,'home.html',context)
    

def get_stats(request,player):
    player = Player.objects.get(name=player)

    df = pd.DataFrame(Player_Team_Stats.objects.all().values()) 
    df = df[df['player_id'] == player.id]

    context = {}
    context['path']   = request.path    
    context['teams']  = df['team'].unique()
    context['player'] = player 
    return render(request,'stats.html',context)


def general_stats(request,player,team):

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    team_df['result']= team_df['result'].apply(lambda x: x[:3])

    if team == 'total':
        df = df
        team_df = team_df[team_df['player_id'] == player.id]

        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]         
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]  
         

    else: 
        df =  df[df['team'] == team ]
        team_df = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)]

        # get goals for        
        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]  

    team_df['goals_for'] = team_df['goals_for'].astype(int)     

    goals_for = team_df['goals_for'].sum()

    context = {} 

    context['Goals']     = int(df['goals'].sum())
    context['Assists']   = int(df['assists'].sum())
    context['Matches']   = int(df['games'].sum())
    context['Ratio_gls'] = round(int(df['goals'].sum()) / int(df['games'].sum()),2)
    context['Ratio_ass'] = round(int(df['assists'].sum()) / int(df['games'].sum()),2)

    total  = int(df['goals'].sum()) + int(df['assists'].sum())
    context['rate_involvement'] = round(total * 100 / goals_for,2)

    return JsonResponse(context)


def gls_as_season(request,player,team):

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    team_df['result']= team_df['result'].apply(lambda x: x[:3])

    if team == 'total':         
        gls_as  = df.groupby(['season']).sum() 
        team_df = team_df[team_df['player_id'] == player.id]  

        # get goals for 
        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]         
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]         
    else: 
        df      = df[df['team'] == team ]
        gls_as  = df.groupby(['season']).sum() 

        team_df = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)] 

        # get goals for        
        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]          

    team_df['goals_for'] = team_df['goals_for'].astype(int)

    team_df = team_df.groupby(['season']).sum() 
    

    context = {}     
        
    context['Goals']    = gls_as['goals'].values.tolist()
    context['Assists']  = gls_as['assists'].values.tolist()    
    context['Seasons']  = gls_as.index.tolist()
    context['Team_gls'] = team_df['goals_for'].values.tolist() 
   
    player_part = []
    for i,b in zip (context['Goals'],context['Assists']): player_part.append(i+b)
    context['Player_part'] =  player_part

    
    return JsonResponse(context)    


def goal_involvements(request,player,team):

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    team_df['result']= team_df['result'].apply(lambda x: x[:3])

    if team == 'total':         
        gls_as  = df.groupby(['season']).sum()
        team_df = team_df[team_df['player_id'] == player.id]        
        
        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]         
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]  
         
 
    else: 
        gls_as  =  df[df['team'] == team ].groupby(['season']).sum()       
        team_df = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)]        

        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]  


    team_df['goals_for'] = team_df['goals_for'].astype(int)  
    team_df = team_df.groupby(['season']).sum()

    context = {}
     
    Goals    = gls_as['goals'].values.tolist()
    Assists  = gls_as['assists'].values.tolist()

    Total_gf = team_df['goals_for'].values.tolist()

    context['Seasons'] = gls_as.index.tolist()

    involvements = []

    for g,a,t in zip(Goals,Assists,Total_gf): 
        try:
            involvements.append( round(( (g + a) * 100) / t , 2))
        except: 
            involvements.append( round(( (g + a) * 100) / 1 , 2))   

    context['involvements'] = involvements

    return JsonResponse(context)   



def performance_competition(request,player,team):

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    context   = {}

    team_df['result'] = team_df['result'].apply(lambda x: x[:3])


    if team == 'total':
        player_df = df.groupby(['competition']).sum().sort_values(by=['games'],ascending=False) 
        team_df   = team_df[team_df['player_id'] == player.id]

        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]           
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]
    
    else: 
        player_df = df[df['team'] == team ].groupby(['competition']).sum().sort_values(by=['games'],ascending=False)
        team_df   = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)]

        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]

    team_df['games'] = 1
    team_df['goals_for'] = team_df['goals_for'].astype(int) 
    team_df  = team_df.groupby(['competition']).sum().sort_values(by=['games'],ascending=False) 
    
    player_df = player_df.drop(['id','player_id'],axis=1)
    

    goals    = player_df['goals'].values.tolist()
    assists  = player_df['assists'].values.tolist()
    team_gls = team_df['goals_for'].values.tolist()

    
    
    performance = []
    for g,a,t in zip(goals,assists,team_gls): 
        try:
            performance.append(round(((g+a)*100) / int(t),2))
        except:
            performance.append(round(((g+a)*100) / 1,2))


    player_df['performance'] = performance 

    

    context['Competition'] = player_df.index.unique().to_list()    
    context['games']       = player_df['games'].values.tolist() 
    context['goals']       = player_df['goals'].values.tolist()
    context['assists']     = player_df['assists'].values.tolist() 
    context['performance'] = player_df['performance'].values.tolist() 

    

    
    return JsonResponse(context)   
