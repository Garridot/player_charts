from database.models import *

from bs4 import BeautifulSoup
import requests
import pandas as pd



# Create your views here.

def Player_Scraping(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    
    res    = requests.get(url,headers=headers)
    soup   = BeautifulSoup(res.content, 'html.parser')
    
    # get the player's name
    player_name = url.split("/")[3].replace('-',' ').title() 
    
    years   = []
    seasons = []    
    # get all seasons he has played  
    options = soup.find('select').find_all('option')    
    for o in options[1:]: 
        years.append(o.get('value'))
        seasons.append(o.text)     
    
    # create the dataframe
    df = pd.DataFrame()
    
    for y,s in zip(years,seasons): 
        
        # format the url 
        path  = f'{url}/plus/0?saison={y}'        
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
                df_1.loc[(df_1['Venue'] == 'A'), 'Home Team'] = df_1['Opponent.1'] 
                df_1.loc[(df_1['Venue'] == 'A'), 'Away Team'] = Team
                df_1.loc[(df_1['Venue'] != 'A'), 'Away Team'] = df_1['Opponent.1']
                df_1.loc[(df_1['Venue'] != 'A'), 'Home Team'] = Team

                # remove unnecessary columns
                df_1 = df_1.drop(['Matchday','For','For.1','Venue','Opponent.1','Opponent','Pos.','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 15','Unnamed: 16','Unnamed: 17'],axis=1) 

                # remove unnecessary rows
                df_1 = df_1[df_1['Date'].str.contains('Squad') == False ]

                # rename columns
                df_1 = df_1.rename(columns={'Unnamed: 9':'Goals','Unnamed: 10':'Assists'})  

                # replace strings
                df_1['Date']   = df_1['Date'].str.replace('/','-') 
                df_1['Result'] = df_1['Result'].str.replace(':','-')

                # insert extra column
                df_1['Competition'] = Competition                

                #reorder columns
                df_1 = df_1[['Date', 'Competition','Home Team','Result','Away Team','Goals','Assists']] 
                
                # insert extra columns
                df_1['Season'] = s.replace('/','-')                 
                df_1['Team']   = Team
                df_1['Player'] = player_name

                df = df.append(df_1)
                
    #replace NaN values with zeros
    df['Goals'], df['Assists'] = df['Goals'].fillna(0), df['Assists'].fillna(0)  
    
    # remove matches that he has not played
    df = df[(df['Goals'].str.contains(r'[0-9]') != False)  | (df['Assists'].str.contains(r'[0-9]') != False)]    
    
    # convert strings to integers
    df['Goals']   = df['Goals'].astype(int)
    df['Assists'] = df['Assists'].astype(int)
    
    # convert  string to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y')
    
    df = df.sort_values(by='Date') 
    
    Save_data(df,player_name)


def Save_data(df,player_name):   

    group  = df.groupby(['Competition','Season','Team']).sum()
    player =  Player.objects.get_or_create(name=player_name)

    # save player's Stats

    for i,x in zip(group.to_dict('records'),group.index.to_list()):

        matches = len(df[(df['Competition']==x[0]) & (df['Season']==x[1])]) 

        stats = Player_Team_Stats(
            player         = player[0],
            team           = x[2],
            competition    = x[0],
            games          = matches,    
            goals          = i['Goals'],
            assists        = i['Assists'],            
            season         = x[1],             
        )
        stats.save()

    # save player's matches
    for i in df.to_dict('records'):

        stats = Player_Matches(
            player         = player[0],
            team           = i['Team'],
            # date           = i['Date'],
            competition    = i['Competition'],
            home_team      = i['Home Team'], 
            result         = i['Result'],
            away_team      = i['Away Team'],
            goals          = i['Goals'],
            assists        = i['Assists'],            
            season         = i['Season'],            
        )
        stats.save() 
    print(f"{player[0]}'s stats saved successfully.")    






        
def call_scrap():
    urls = [
        # Messi's Stats
        'https://www.transfermarkt.com/lionel-messi/leistungsdaten/spieler/28003',
        # Cristiano's Stats
        'https://www.transfermarkt.com/cristiano-ronaldo/leistungsdaten/spieler/8198',    
        # Ibrahimovic's Stats
        'https://www.transfermarkt.com/zlatan-ibrahimovic/leistungsdaten/spieler/3455',
        #Suarez's Stats
        'https://www.transfermarkt.com/luis-suarez/leistungsdaten/spieler/44352',
        # Lewandowski's Stats
        'https://www.transfermarkt.com/robert-lewandowski/leistungsdaten/spieler/38253',
        # Henry's Stats
        'https://www.transfermarkt.com/thierry-henry/leistungsdaten/spieler/3207',
        # Agüero's Stats
        'https://www.transfermarkt.com/sergio-aguero/leistungsdaten/spieler/26399',
        # Rooney's Stats
        'https://www.transfermarkt.com/wayne-rooney/leistungsdaten/spieler/3332',       
        # Benzema's Stats
        'https://www.transfermarkt.com/karim-benzema/leistungsdaten/spieler/18922',
    ]

    for url in urls:
        Player_Scraping(url)
