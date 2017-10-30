Concept of the betting program:

Get accountID of all players playing in tournaments which can be bet on <br />
Find all their games played in the current season and store in DB<br />
Get all the challenger league players' games for extra data about matchup statistics (assuming the challenger players and tournament<br />
  level players are similar in skill)<br />
Using these stats determine the % chance of champ X beating champ Y<br />
Add up these stats in a 1v1 based performance (5 series of 1v1's)<br />
Use some method to determine which team will win the game<br />
Pull data from some betting website regarding odds of winning/losing<br />
More math to determine when its worth betting (beating house %)<br />
Automatically place the bets based on selected champs<br />
  ---May have to integrate image recognition on streams or else this will be manual -residentsleeper<br />

Right now its using a sqlite db with python.<br />
there should be a constant python script running scraping active high level games and placing it in the db and stored on a server<br />
  so we can all access identical data. Might have to have a 2nd DB for pro level tournament games if those aren't in API (because offline<br />
  mode is usually used for tournies iirc). Using these DB's we can do math and have a few testing strategies given two list inputs<br />
  where team1 = "champ1,champ2,champ3,champ4,champ5" and team2 = "champ1,champ2,champ3,champ4,champ5" to predict which team wins<br />
