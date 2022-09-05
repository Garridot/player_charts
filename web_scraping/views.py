from django.http import HttpResponse
from django.shortcuts import render
from database.models import *

from bs4 import BeautifulSoup
import requests
import pandas as pd



# Create your views here.

old_season = ['94-95', '95-96', '96-97' ,'97-98', '98-99' ,'99-00', '00-01', '01-02', '02-03',
 '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12',
 '12-13', '13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23']
new_season = ['1994-95', '1995-96', '1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02' ,'2002-03',
 '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10' ,'2010-11' ,'2011-12',
 '2012-13', '2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']


def get_url_scraping(request):    
    
    if request.user.is_authenticated:
        if request.method == 'POST': 
           
            url    = request.POST['url']            
            if url == '': 
                return HttpResponse("Url does not exist." )
            else:    
                player = url.split("/")[3].replace('-',' ').title()

                player_scraping(url,update=False)

                return HttpResponse(f"{player}'s stats added successfully." )

        return render(request,'form_scraping.html')
       
    else:
        return HttpResponse("User must to be login" )


def player_scraping(url,update):
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36" }
    
    res    = requests.get(url,headers=headers)
    soup   = BeautifulSoup(res.content, 'html.parser')
    
    # get the player's name
    player_name = url.split("/")[3].replace('-',' ').title() 
    
   

    if update == True:
        # get the last season he has played  
        season = soup.find('select').find_all('option')[1].text
        year   = soup.find('select').find_all('option')[1].get('value')

        get_data(url,headers,year,season,player_name)

    else:  
        # get all seasons he has played  
        years   = []
        seasons = [] 

        options = soup.find('select').find_all('option') 

        for o in options[1:]: 
            years.append(o.get('value'))
            seasons.append(o.text)  

        for year,season in zip(years,seasons): 

            get_data(url,headers,year,season,player_name)
      

def get_data(url,headers,year,season,player_name): 

    # create the dataframe
    df = pd.DataFrame()

    # format the url 
    path  = f'{url}/plus/0?saison={year}'        
    res   = requests.get(path,headers=headers)
    soup  = BeautifulSoup(res.content, 'html.parser')
    boxes = soup.find('div',class_='large-8 columns').find_all('div',class_='box')   

    
    for b in boxes[2:]: 
        
        # get competition
        try:
            Competition = b.find('div',class_='table-header img-vat').find('img').get("title")
        except:
            Competition = b.find('div',class_='table-header img-vat').find('a').text.strip()                 


        Team  = b.find_all('td',class_='zentriert')[3].find('a').get('title')

        table = b.find_all('table')

        for i in table:

            df_1 = pd.read_html(str(i))
            df_1 = df_1[0]

            # delete unnecessary string based on condition
            try:
                df_1.loc[df_1['Opponent.1'].astype(str).str[-1] == ')', 'Opponent.1'] = df_1['Opponent.1'].apply(lambda x: "" + x[:-5])
            except:
                None

            # insert new columns based on conditions
            df_1.loc[(df_1['Venue'] == 'A'), 'home_team'] = df_1['Opponent.1'] 
            df_1.loc[(df_1['Venue'] == 'A'), 'away_team'] = Team
            df_1.loc[(df_1['Venue'] != 'A'), 'away_team'] = df_1['Opponent.1']
            df_1.loc[(df_1['Venue'] != 'A'), 'home_team'] = Team

            # remove unnecessary columns
            df_1 = df_1.drop(['Matchday','For','For.1','Venue','Opponent.1','Opponent','Pos.','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 15','Unnamed: 16','Unnamed: 17'],axis=1) 

            # remove unnecessary rows
            df_1 = df_1[df_1['Date'].str.contains('Squad') == False ]

            # rename columns
            df_1 = df_1.rename(columns={'Unnamed: 9':'goals','Unnamed: 10':'assists','Date':'date','Result':'result'})  

            # replace strings
            df_1['date']   = df_1['date'].str.replace('/','-') 
            df_1['result'] = df_1['result'].str.replace(':','-')

            # insert extra column
            df_1['competition'] = Competition                

            #reorder columns
            df_1 = df_1[['date', 'competition','home_team','result','away_team','goals','assists']] 
            
            # insert extra columns
            df_1['season'] = season.replace('/','-')                 
            df_1['team']   = Team
            df_1['player'] = player_name

            df = df.append(df_1)
                
    #replace NaN values with zeros
    df['goals'], df['assists'] = df['goals'].fillna(0), df['assists'].fillna(0)  
    
    # remove matches that he has not played
    df = df[(df['goals'].str.contains(r'[0-9]') != False)  | (df['assists'].str.contains(r'[0-9]') != False)]    
    
    # convert strings to integers
    df['goals']   = df['goals'].astype(int)
    df['assists'] = df['assists'].astype(int)
    
    # convert  string to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m-%d-%y')
    
    df = df.sort_values(by='date')    

    save_data(df,player_name)
   


def save_data(df,player_name):

    player =  Player.objects.get_or_create(name=player_name) 

    team_df = df
    
    team_df['season'] = team_df['season'].replace(old_season,new_season)   
    
    team_df['games'] = 1

    home_df = team_df.loc[team_df['home_team'] == team_df['team']]    

    if len(home_df) !=  0:

        home_df['team_goals']   = home_df['result'].astype(str).str.split("-").str[0]
        home_df['team_goals']   = home_df['team_goals'].astype(int)

        home_df['goals_againt']  = home_df['result'].astype(str).str.split("-").str[1]
        home_df['goals_againt']  = home_df['goals_againt'].str.replace(r'[A-Za-z]','')
        home_df['goals_againt']  = home_df['goals_againt'].astype(int)  

        home_df.loc[home_df['team_goals'] > home_df['goals_againt'], 'wins'] = int(1)
        home_df.loc[home_df['team_goals'] < home_df['goals_againt'] , 'defeats'] = int(1)
        home_df.loc[home_df['team_goals'] == home_df['goals_againt'] , 'draws'] = int(1)  


    away_df = team_df.loc[team_df['home_team'] != team_df['team']]

    if len(away_df) !=  0:

        away_df['team_goals']   = away_df['result'].astype(str).str.split("-").str[1]
        away_df['team_goals']   = away_df['team_goals'].str.replace(r'[A-Za-z]','')
        away_df['team_goals']   = away_df['team_goals'].astype(int)

        away_df['goals_againt']  = away_df['result'].astype(str).str.split("-").str[0]
        away_df['goals_againt']  = away_df['goals_againt'].astype(int) 
    
        away_df.loc[away_df['team_goals'] > away_df['goals_againt'], 'wins'] = int(1)
        away_df.loc[away_df['team_goals'] < away_df['goals_againt'] , 'defeats'] = int(1)
        away_df.loc[away_df['team_goals'] == away_df['goals_againt'] , 'draws'] = int(1)

    df = home_df.append(away_df)   

    df = df.groupby(['team','competition','season']).sum()       

    for record,index in zip(df.to_dict('records'),df.index.to_list()):        

        Player_Stats_by_Season.objects.filter().update()
        Player_Stats_by_Season.objects.update_or_create(
            player         = player[0],
            team           = index[0],
            competition    = index[1],               
            goals          = record['goals'],
            assists        = record['assists'],  
            games          = record['games'], 
            wins           = record['wins'],  
            draws          = record['draws'],
            defeats        = record['defeats'],
            team_goals     = record['team_goals'],          
            season         = index[2],             
        )

        print(f"{player[0]}'s stats {index[2]} updated successfully.")  
   
        
def update_players():
    urls = [
        # Messi's Stats
        'https://www.transfermarkt.com/lionel-messi/leistungsdaten/spieler/28003',
        # Cristiano's Stats
        'https://www.transfermarkt.com/cristiano-ronaldo/leistungsdaten/spieler/8198',    
        # # Ibrahimovic's Stats
        'https://www.transfermarkt.com/zlatan-ibrahimovic/leistungsdaten/spieler/3455',
        # #Suarez's Stats
        'https://www.transfermarkt.com/luis-suarez/leistungsdaten/spieler/44352',
        # Lewandowski's Stats
        'https://www.transfermarkt.com/robert-lewandowski/leistungsdaten/spieler/38253',  
        # Benzema's Stats
        'https://www.transfermarkt.com/karim-benzema/leistungsdaten/spieler/18922',
        # Mbappe's Stats
        'https://www.transfermarkt.co.in/kylian-mbappe/leistungsdaten/spieler/342229',
        # Neymar's Stats
        'https://www.transfermarkt.co.in/neymar/leistungsdaten/spieler/68290',
        # Drogba's Stats
        # 'https://www.transfermarkt.co.in/didier-drogba/leistungsdaten/spieler/3924',  
        # Haaland's Stats
        'https://www.transfermarkt.co.in/erling-haaland/leistungsdaten/spieler/418560',  
        # Muller's Stats
        'https://www.transfermarkt.co.in/thomas-muller/leistungsdaten/spieler/58358',
        # Etoo's Stats
        # 'https://www.transfermarkt.co.in/samuel-etoo/leistungsdaten/spieler/4257'
        
    ]

    for url in urls:
        player_scraping(url,update=True)



# update_players()