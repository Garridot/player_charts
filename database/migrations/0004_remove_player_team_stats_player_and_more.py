# Generated by Django 4.0.5 on 2022-09-04 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_player_stats_by_season'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player_team_stats',
            name='player',
        ),
        migrations.DeleteModel(
            name='Player_Matches',
        ),
        migrations.DeleteModel(
            name='Player_Team_Stats',
        ),
    ]