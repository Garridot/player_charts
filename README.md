# FOOTBALL PLAYER CHARTS
Football Player Charts is a football statistics website where you will find information, statistics, and charts that show how influenced a player in each team he played.

## HOW IT WORKS?

On the Frontend,  it shows the data through a request to an API. Using the Charts.js library, the data is shown in graphics for better compression.

On the Backend, the API was built in Django rest framework, through ORM, it connects to the database, gets the data, and returns the result (matches, goals, assists, percent of goal involvements in total and by season. The percent of the goals scored in the team, favorite victims, performance by competition, and the percent of goals and assists per game of the player) in a JSON response.
By collecting all the data through Web Scraping, this is a consumption-only API — only the HTTP GET method is available.

The project is deployed on Heroku, for which it's using PostgreSQL database that provides Heroku.

## HOW THE DATA IS COLLECTED?
The data is collected and it's updated through a web scraping on transfermarkt.com. All terms and conditions you can be read here.

## ENDPOINTS

Base URL for all endpoints https://football-player-graphics.herokuapp.com/

* GET /general_stats/{player_name}/{team}
* GET /gls_as_season/{player_name}/{team}
* GET /goal_involvements/{player_name}/{team}
* GET /performance_competition/{player_name}/{team}
* GET /favorite_victims/{player_name}/{team}
* GET /rate_goals/{player_name}/{team}