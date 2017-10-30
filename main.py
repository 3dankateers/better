"""

"""
import zlib
import zmq
import simplejson
import json
import urllib
import sys

import sqlite3
conn = sqlite3.connect('data/League.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS test2 (summonerID, playerName, role, season, champion, lane);")
conn.commit()


API_KEY = "RGAPI-ee771521-37c9-4c27-b826-2e6ae442a45c"

CHALLENGER_LEAGUE = "https://na1.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + API_KEY

def main():
	#Get summoner IDs from challenger league
	url = CHALLENGER_LEAGUE

	response = urllib.urlopen(url)
	data = simplejson.loads(response.read())
	entries = data["entries"]
	for rows in range (len(entries)):
		summonerID = entries[rows]['playerOrTeamId']
		#Replace name with a questionmark if it cant be encoded, koreans playing this game reeeeee
		playerName = entries[rows]['playerOrTeamName'].encode(sys.stdout.encoding, errors = 'replace')

		#PlayerID to accountID conversion
		SUMMONER_V3 = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/" + summonerID + "?api_key=" + API_KEY

		url = SUMMONER_V3
		response = urllib.urlopen(url)
		data = simplejson.loads(response.read())
		summonerdata = data

		playerID = summonerdata["accountId"]
		#print playerID

		#After you hvae the ID's get their match history
		ACCOUNT_MATCH_LIST = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(playerID)+"?api_key="+API_KEY

		url = ACCOUNT_MATCH_LIST
		response = urllib.urlopen(url)
		data = simplejson.loads(response.read())
		matches = data["matches"]

		#print matches[0]['role']


		for rows in range (len(matches)):
			role = matches[rows]['role']
			season = matches[rows]['season']
			champion = matches[rows]['champion']
			lane = matches[rows]['lane']
			
			#shove data into sqlite
			c.execute("INSERT INTO test2 VALUES (?,?,?,?,?,?);", (summonerID, playerName, role, season, champion, lane))
			conn.commit()
			#print role
			#print season
			#print champion
			#print lane

	#close connection to sqlite
	f.close();
	conn.close();


if __name__ == '__main__':
	main()