"""

"""
#Used to change json to python dicts for easier reading
import json
#Gets the json file and headers from html
import urllib
#For passing parameters into the program later and the emergency close in rate limiter
import sys
import sqlite3
#waiting
import time

conn2 = sqlite3.connect('data/GameIDs.sqlite')
c = conn2.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Games (gameID UNIQUE, season, champ1, champ2, champ3, champ4, champ5, champ6, champ7, champ8, champ9, champ10, winner, gameVersion, firstBlood);")
conn2.commit()

#ACCOUNT_MATCH_LIST = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(playerID)+"?api_key="+API_KEY

#GET_GAME_STATS_FROM_ID = "https://na1.api.riotgames.com/lol/match/v3/matches/"+gameID+"?api_key="+API_KEY



def main():
	#name of sqlite db
    database = 'data/Challengers.sqlite'
    # create a database connection
    conn = create_connection(database)
    with conn:
        playerList = select_accountID(conn)



	for rows in range (len(playerList)):
		ACCOUNT_MATCH_LIST = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(playerList[rows])+"?api_key="+API_KEY

		url = ACCOUNT_MATCH_LIST
		response = urllib.urlopen(url)

		data = json.loads(response.read())


		matches = data["matches"]

		ChampID = [0,0,0,0,0,0,0,0,0,0]

		for rows in range (len(matches)):
			try:
				gameID = matches[rows]['gameId']
				GET_GAME_STATS_FROM_ID = "https://na1.api.riotgames.com/lol/match/v3/matches/"+str(gameID)+"?api_key="+API_KEY
				url = GET_GAME_STATS_FROM_ID
				response = urllib.urlopen(url)
				dontgetbanned(response)
				data = json.loads(response.read())
				season = data["seasonId"]
				gameVersion = data["gameVersion"]

				for player in range(len(data["participants"])):
					ChampID[player] = data["participants"][player]['championId']


				'''
				Champ 1 = Top
				Champ 2 = Jung
				Champ 3 = Mid
				Champ 4 = ADC
				Champ 5 = Support
				Winner 100 = team 1-5
				200 = team 6-10
				'''
				if(data["teams"][0]["win"]=="Win"):
					winner = 100
				else:
					winner = 200
				if(data["teams"][0]["firstBlood"]):
					firstBlood = 100
				else:
					firstBlood = 200

				c.execute("INSERT OR IGNORE INTO Games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (gameID, season, ChampID[0], ChampID[1], ChampID[2], ChampID[3], ChampID[4], ChampID[5], ChampID[6], ChampID[7], ChampID[8], ChampID[9], winner, gameVersion, firstBlood))
				conn2.commit()
				time.sleep(1)
			except KeyError:
				print data



def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return None

def select_accountID(conn):
    cur = conn.cursor()
    cur.execute("SELECT accountID FROM ChallengerLeague")
 
    rows = cur.fetchall()
    playerList = []

    for row in rows:
    	stringRow = str(row)
    	stringRow.strip(',')

    	playerList.append(list(row)[0])
        #print(row)

    return playerList

def dontgetbanned(response):
	#Gets data from league API headers, contains limit and how much youve used
	curAppCount = response.info().getheader('X-App-Rate-Limit-Count')
	curAppLimit = response.info().getheader('X-App-Rate-Limit')
	x = curAppCount.split(',')
	RequestsPerSecond = x[1].split(':')
	RequestsPerMinute = x[0].split(':')
	x = curAppLimit.split(',')
	MaxRequestsPerSecond = x[1].split(':')
	MaxRequestsPerMinute = x[0].split(':')

	if(int(RequestsPerMinute[0])>(int(MaxRequestsPerMinute[0])-2)):
		print "Rate too high"
		time.sleep(30)

	if(int(RequestsPerSecond[0])>(int(MaxRequestsPerSecond[0])-2)):
		print "Rate too high"
		time.sleep(5)

if __name__ == '__main__':
	main()
