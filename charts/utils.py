
def get_goal_involvements_rate(stats):    
    
    # group by season all matches
    df = stats.groupby(['season']).sum()

    context = {}    
     
    Goals    = df['goals'].values.tolist()
    Assists  = df['assists'].values.tolist()
    Total_gf = df['team_goals'].values.tolist()    

    involvements = []
    for g,a,t in zip(Goals,Assists,Total_gf): 

        involvements.append(g + a)

        # if 'Total_gf' is equal to 0, replace to 1(You can not divide by zero)                  
        # try:    involvements.append( round(( (g + a) * 100) / t , 2))
        # except: involvements.append( round(( (g + a) * 100) / 1 , 2))   

    context['seasons']      = df.index.tolist()
    context['goal_involvements_rate'] = involvements

    return context

def get_ages(df,age):    

    list_age = []

    df = df.groupby(['season']).sum() 

    for i in range(len(df.index.tolist())): 
        a = (age - i) 
        list_age.append(a)   

    return list_age     