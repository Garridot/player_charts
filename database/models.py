from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
import datetime

# Create your models here.

def location_media(instance,filename):
    return f"players/{instance.name}/{filename}"  

class Player(models.Model):
    name        = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    picture     = models.ImageField(blank=True,null=True, upload_to=location_media) 

    def __str__(self):
        return self.name


class Player_Team_Stats(models.Model):
    player         = models.ForeignKey(Player,on_delete=models.CASCADE)
    team           = models.CharField(max_length=100)
    competition    = models.CharField(max_length=100)
    games          = models.IntegerField()    
    goals          = models.IntegerField()
    assists        = models.IntegerField()    
    season         = models.CharField(max_length=100)   


class Player_Matches(models.Model):
    player         = models.ForeignKey(Player,on_delete=models.CASCADE)
    team           = models.CharField(max_length=100)
    date           = models.DateField(default=datetime.date.today) 
    competition    = models.CharField(max_length=100)
    home_team      = models.CharField(max_length=100)
    result         = models.CharField(max_length=100)
    away_team      = models.CharField(max_length=100)
    goals          = models.IntegerField()
    assists        = models.IntegerField()    
    season         = models.CharField(max_length=100) 


class Player_Stats_by_Season(models.Model):
    player         = models.ForeignKey(Player,on_delete=models.CASCADE)
    team           = models.CharField(max_length=100)    
    competition    = models.CharField(max_length=100)    
    goals          = models.IntegerField()
    assists        = models.IntegerField()
    games          = models.IntegerField()    
    wins           = models.IntegerField()    
    draws          = models.IntegerField()
    defeats        = models.IntegerField()  
    team_goals     = models.IntegerField()  
    season         = models.CharField(max_length=100)