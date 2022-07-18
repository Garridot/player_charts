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

    # return the overall stats of the player in a required team

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    # get only the goals 
    team_df['result']= team_df['result'].apply(lambda x: x[:3])

    if team == 'total':
        # if the request is 'total', get all the matches he played 
        team_df = team_df[team_df['player_id'] == player.id]
        
        # get all team's goals for  
        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]         
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]
    
    else: 
        # get all the player's stats in the required team 
        df =  df[df['team'] == team ]        
        
        # get all the matches he played in the required team 
        team_df = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)]
        
        # get team's goals for          
        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]  

    # convert strings to integers
    team_df['goals_for'] = team_df['goals_for'].astype(int)
    # sum all teams's goals  
    goals_for = team_df['goals_for'].sum()
    # sum(gls + assists) 
    total  = int(df['goals'].sum()) + int(df['assists'].sum())

    context = {} 
    context['Goals']     = int(df['goals'].sum())
    context['Assists']   = int(df['assists'].sum())
    context['Matches']   = int(df['games'].sum())
    context['Ratio_gls'] = round(int(df['goals'].sum()) / int(df['games'].sum()),2)
    context['Ratio_ass'] = round(int(df['assists'].sum()) / int(df['games'].sum()),2)
    
    # calculate the goals involvements %
    context['rate_involvement'] = round(total * 100 / goals_for,2)

    return JsonResponse(context)




def gls_as_season(request,player,team):

    # return all player's goals, player's assists, player's goals involvements and all team's goals by season   

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    team_df['result']= team_df['result'].apply(lambda x: x[:3])

    if team == 'total':     
        # if the request is 'total', get all player's stats by season    
        gls_as  = df.groupby(['season']).sum() 

        # get all the matches he played  
        team_df = team_df[team_df['player_id'] == player.id]  

        # get all team's goals 
        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]         
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]         
    
    else:         
        # get all player's stats in the required team  by season   
        gls_as  = df[df['team'] == team ].groupby(['season']).sum() 

        # get all the matches he played in the required team 
        team_df = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)] 

        # get all team's goals        
        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]          

    # convert strings to integers
    team_df['goals_for'] = team_df['goals_for'].astype(int)

    

    # group by season all matches 
    team_df = team_df.groupby(['season']).sum()

    context = {}     
        
    context['Goals']    = gls_as['goals'].values.tolist()
    context['Assists']  = gls_as['assists'].values.tolist()    
    context['Seasons']  = gls_as.index.tolist()
    context['Team_gls'] = team_df['goals_for'].values.tolist() 
   
    player_part = []
    # get goals involvements by season
    for i,b in zip (context['Goals'],context['Assists']): player_part.append(i+b)    
    context['Player_part'] =  player_part

    
    return JsonResponse(context)    


def goal_involvements(request,player,team):
    # return the rate of goals involvements by season     

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    team_df['result']= team_df['result'].apply(lambda x: x[:3])    

    if team == 'total':     
        # get all player's stats by season         
        gls_as  = df.groupby(['season']).sum() 
        # get all the matches he played  
        team_df = team_df[team_df['player_id'] == player.id]        
        
        # get all team's goals        
        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]         
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]  
         
 
    else: 
        # get all player's stats in the required team  by season  
        gls_as  =  df[df['team'] == team ].groupby(['season']).sum()      

        # get all the matches he played in the required team 
        team_df = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)]        

        # get all team's goals   
        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]  

    # convert strings to integers
    team_df['goals_for'] = team_df['goals_for'].astype(int)  
    
    # group by season all matches
    team_df = team_df.groupby(['season']).sum()

    context = {}    
     
    Goals    = gls_as['goals'].values.tolist()
    Assists  = gls_as['assists'].values.tolist()
    Total_gf = team_df['goals_for'].values.tolist()    

    involvements = []
    for g,a,t in zip(Goals,Assists,Total_gf): 

        # if 'Total_gf' is equal to 0, replace to 1(You can not divide by zero)                  
        try:    involvements.append( round(( (g + a) * 100) / t , 2))
        except: involvements.append( round(( (g + a) * 100) / 1 , 2))   

    context['Seasons']      = gls_as.index.tolist()
    context['involvements'] = involvements

    return JsonResponse(context)   





def performance_competition(request,player,team):

    # return all player's goals, player's assists, player's goals involvements and player's matches by competition

    player = Player.objects.get(name=player)
    
    df = pd.DataFrame(Player_Team_Stats.objects.all().values())    
    
    df = df[df['player_id'] == player.id]

    team_df = pd.DataFrame(Player_Matches.objects.all().values()) 

    context   = {}

    team_df['result'] = team_df['result'].apply(lambda x: x[:3])


    if team == 'total':
        # get all player's stats by competition 
        player_df = df.groupby(['competition']).sum().sort_values(by=['games'],ascending=False) 
        # get all player's matches
        team_df   = team_df[team_df['player_id'] == player.id]
        
        # get all team's goals
        team_df.loc[team_df['home_team'] == team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[0]           
        team_df.loc[team_df['away_team' ]== team_df['team'], 'goals_for'] = team_df['result'].astype(str).str[2]
    
    else: 
        # get all player's stats in the required team  by competition
        player_df = df[df['team'] == team ].groupby(['competition']).sum().sort_values(by=['games'],ascending=False)
        # get all player's matches in the required team 
        team_df   = team_df[(team_df['player_id'] == player.id) & (team_df['team'] == team)]
        
        # get all team's goals
        team_df.loc[(team_df['home_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[0]
        team_df.loc[(team_df['away_team'] == team), 'goals_for'] = team_df['result'].astype(str).str[2]

    team_df['games'] = 1
    # convert strings to integers
    team_df['goals_for'] = team_df['goals_for'].astype(int) 

    # group by season all competition
    team_df  = team_df.groupby(['competition']).sum().sort_values(by=['games'],ascending=False) 
    
    player_df = player_df.drop(['id','player_id'],axis=1)
    

    goals    = player_df['goals'].values.tolist()
    assists  = player_df['assists'].values.tolist()
    team_gls = team_df['goals_for'].values.tolist()

    
    
    performance = []
    for g,a,t in zip(goals,assists,team_gls): 
        # if 'team_gls' is equal to 0, replace to 1(You can not divide by zero)  
        try:    performance.append(round(((g+a)*100) / int(t),2))
        except: performance.append(round(((g+a)*100) / 1,2))


    player_df['performance'] = performance 

    

    context['Competition'] = player_df.index.unique().to_list()    
    context['games']       = player_df['games'].values.tolist() 
    context['goals']       = player_df['goals'].values.tolist()
    context['assists']     = player_df['assists'].values.tolist() 
    context['performance'] = player_df['performance'].values.tolist() 

    

    
    return JsonResponse(context)   
