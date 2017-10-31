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

conn = sqlite3.connect('data/GameIDs.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Games (gameID, season, champ1, champ2, champ3, champ4, champ5, champ6, champ7, champ8, champ9, champ10, winner, gameVersion);")
conn.commit()

#Gunna need to update this everyday, fun
API_KEY = "RGAPI-ee771521-37c9-4c27-b826-2e6ae442a45c"

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

		for rows in range (len(matches)):
			gameID = matches[rows]['gameID']
			#logging("Row " + str(rows) + " inserted into Challenger.sqlite")

			GET_GAME_STATS_FROM_ID = "https://na1.api.riotgames.com/lol/match/v3/matches/"+gameID+"?api_key="+API_KEY
			url = ACCOUNT_MATCH_LIST
			response = urllib.urlopen(url)
			data = json.loads(response.read())


			season = data["seasonId"]
			gameVersion = data["gameVersion"]
			participants = data["participants"]


			'''
			Champ 1 = Top
			Champ 2 = Jung
			Champ 3 = Mid
			Champ 4 = ADC
			Champ 5 = Support
			Winner 100 = team 1-5
			200 = team 6-10
			'''
			c.execute("INSERT INTO Games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (gameID, season, champ1, champ2, champ3, champ4, champ5, champ6, champ7, champ8, champ9, champ10, winner, gameVersion))
			conn.commit()



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

if __name__ == '__main__':
	main()