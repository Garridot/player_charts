def utils_generalstats(player,df):

    context = {}

    context['player']       = player.name
    context['matches']      = 0  
    context['goals']        = 0
    context['assists']      = 0
    context["team_goals"] = 0
    
     

    for i in df['games']     : context['matches'] += i
    for i in df['goals']     : context['goals']   += i 
    for i in df['assists']   : context['assists'] += i
    for i in df['team_goals']: context["team_goals"] += i 


    context["involvement"] = round((context['goals'] + context['assists']) * 100 /  context["team_goals"],2)    
    

    return context


def utils_statscompet(player,df):
    df = df.groupby(['competition']).sum()  
    
    
    context = {}

    context['player']       = player.name  
    context['competition']  = df.index.unique().to_list() 
    context['games']        = df['games'].values.tolist() 
    context['goals']        = df['goals'].values.tolist() 
    context['assists']      = df['assists'].values.tolist()

    return context
    



def utils_involvement_season(player,df):    
    
    # group by season all matches
    df = df.groupby(['season']).sum()

    seasons = []   

    for i in range(len(df.index.tolist())):
        seasons.append(f"Season {i+1}")  

    context = {}    
     
    context['player']  = player.name  
    context['goals']   = df['goals'].values.tolist()
    context['assists'] = df['assists'].values.tolist() 
    context['seasons'] = seasons 

    return context



