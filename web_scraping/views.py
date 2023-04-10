from django.http import HttpResponse
from django.shortcuts import render
from database.models import *

from bs4 import BeautifulSoup
import requests
import pandas as pd

import validators
from validators import ValidationFailure


# Create your views here.

old_season = ['94-95', '95-96', '96-97' ,'97-98', '98-99' ,'99-00', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12',
                '12-13', '13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23']

new_season = ['1994-95', '1995-96', '1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02' ,'2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10' ,'2010-11' ,'2011-12',
                '2012-13', '2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']

     




class Player_Charts_Scraping():

    def __init__(self,url,update):
        self.url = url   
        self.update = update 

    @property
    def url(self):
        return self.__url   


    def validate_url(self):
        result = validators.url(self.__url)
        if isinstance(result, ValidationFailure):
            print('Failed URL: invalid url.')
            return False  
        else:
            return True              


    @url.setter
    def url(self,url):
        self.__url = url


    def get_player_name(self):
            # get the player's name
            player_name = self.url.split("/")[3].replace('-',' ').title()          
            return player_name


    def if_update(self,soup):
        if self.update == True:
        # get the last season he has played              
            year   = soup.find('select').find_all('option')[1].get('value')
            season = soup.find('select').find_all('option')[1].text
            self.web_scraping(year,season)

        else:  
            # get all seasons he has played
            lists = soup.find('select').find_all('option') 
            years   = []  
            seasons = []

            for i in lists[1:]:  years.append(i.get('value')),seasons.append(i.text)  
            for year,season in zip(years,seasons): self.web_scraping(year,season) 


    def web_scraping(self,year=None,season=None):

        if self.validate_url():

            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} 
            
            if year == None: url = self.url
            else: 
                url = f'{self.url}/plus/0?saison={year}'
                
            res    = requests.get(url,headers=headers)
            soup   = BeautifulSoup(res.content, 'html.parser')

            if year == None: self.if_update(soup)
            else: 
                self.get_data(soup,season)
            

    def get_data(self,soup,season): 

        # create the dataframe
        df = pd.DataFrame()

        boxes = soup.find('div',class_='large-8 columns').find_all('div',class_='box')   
    
        for box in boxes[2:]:
                  
            competition = box.find('div',class_='table-header img-vat').find('a').text.strip()              
            team   = box.find_all('td',class_='zentriert')[3].find('a').get('title')            
            tables = box.find_all('table')

            for i in tables:

                df_1 = pd.read_html(str(i))
                df_1 = df_1[0]

                # insert extra column
                df_1['competition'] = competition  
                df_1['season']      = season.replace('/','-')                 
                df_1['team']        = team                

                df = df.append(df_1)        

        self.clean_data(df)


    def clean_data(self,df): 

        # remove unnecessary rows
        df = df[df['Date'].str.contains('Squad') == False ]
        
        # remove unnecessary columns
        df = df.drop(['Date','Matchday','For','For.1','Opponent.1','Opponent','Pos.','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 15','Unnamed: 16','Unnamed: 17'],axis=1)   

        # rename columns        
        df = df.rename(columns={'Unnamed: 9':'goals','Unnamed: 10':'assists','Result':'result'})  

        # replace NaN values with zeros
        df['goals'], df['assists'] = df['goals'].fillna(0), df['assists'].fillna(0)   

         

        # remove matches he has not played
        try: df = df[(df['goals'].str.contains(r'[0-9]') != False)  | (df['assists'].str.contains(r'[0-9]') != False)] 
        except:None

        # convert strings to integers
        df['goals']   = df['goals'].astype(int)
        df['assists'] = df['assists'].astype(int)

        # replace season values
        df['season'] = df['season'].replace(old_season,new_season)   

        df['games'] = 1

        

        # get the games when he played as home team
        home_df = df.loc[df['Venue'] == 'H']  
        if len(home_df) != 0: 
            home_df['team_goals']   = home_df['result'].astype(str).str.split(":").str[0]
            home_df['team_goals']   = home_df['team_goals'].str.replace(r'[A-Za-z]','')
            home_df['team_goals']   = home_df['team_goals'].astype(int)

            home_df['goals_againt']  = home_df['result'].astype(str).str.split(":").str[1]
            home_df['goals_againt']  = home_df['goals_againt'].str.replace(r'[A-Za-z]','')
            home_df['goals_againt']  = home_df['goals_againt'].astype(int)  

            home_df.loc[home_df['team_goals'] > home_df['goals_againt'], 'wins'] = int(1)
            home_df.loc[home_df['team_goals'] < home_df['goals_againt'] , 'defeats'] = int(1)
            home_df.loc[home_df['team_goals'] == home_df['goals_againt'] , 'draws'] = int(1)  


        # get the games when he played as away team
        away_df = df.loc[df['Venue'] == 'A']  
        if len(away_df) != 0:   
            away_df['team_goals']   = away_df['result'].astype(str).str.split(":").str[1]
            away_df['team_goals']   = away_df['team_goals'].str.replace(r'[A-Za-z]','')
            away_df['team_goals']   = away_df['team_goals'].astype(int)

            away_df['goals_againt']  = away_df['result'].astype(str).str.split(":").str[0]
            away_df['goals_againt']  = away_df['goals_againt'].astype(int) 
        
            away_df.loc[away_df['team_goals'] > away_df['goals_againt'], 'wins'] = int(1)
            away_df.loc[away_df['team_goals'] < away_df['goals_againt'] , 'defeats'] = int(1)
            away_df.loc[away_df['team_goals'] == away_df['goals_againt'] , 'draws'] = int(1)


        # create new df
        df_2 = home_df.append(away_df) 

        # remove unnecessary columns
        df_2 = df_2.drop(['Venue','goals_againt'],axis=1)   

        df_2 = df_2.groupby(['team','competition','season']).sum()  

        self.save_date(df=df_2)


    def save_date(self,df):
        player_name = self.get_player_name()

        
        player =  Player.objects.get_or_create(name=player_name)


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

            print(f"{player[0]}'s stats {index[1]} {index[2]} updated successfully.")      




def update_players():

    urls = [
        # Messi's Stats
        'https://www.transfermarkt.com/lionel-messi/leistungsdaten/spieler/28003',
        # Cristiano's Stats
        'https://www.transfermarkt.com/cristiano-ronaldo/leistungsdaten/spieler/8198',    
        # Ibrahimovic's Stats
        'https://www.transfermarkt.com/zlatan-ibrahimovic/leistungsdaten/spieler/3455',
        # Suarez's Stats
        'https://www.transfermarkt.com/luis-suarez/leistungsdaten/spieler/44352',
        # Lewandowski's Stats
        'https://www.transfermarkt.com/robert-lewandowski/leistungsdaten/spieler/38253',  
        # Benzema's Stats
        'https://www.transfermarkt.com/karim-benzema/leistungsdaten/spieler/18922',
        # Mbappe's Stats
        'https://www.transfermarkt.co.in/kylian-mbappe/leistungsdaten/spieler/342229',
        # Neymar's Stats
        'https://www.transfermarkt.co.in/neymar/leistungsdaten/spieler/68290',         
        # Haaland's Stats
        'https://www.transfermarkt.co.in/erling-haaland/leistungsdaten/spieler/418560',  
        # Muller's Stats
        'https://www.transfermarkt.co.in/thomas-muller/leistungsdaten/spieler/58358',
    ]

    for url in urls: Player_Charts_Scraping(url,update=True).web_scraping() 



update_players()




