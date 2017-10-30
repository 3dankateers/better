"""

"""
#Used to change json to python dicts for easier reading
import json
#Gets the json file and headers from html
import urllib
#For passing parameters into the program later and the emergency close in rate limiter
import sys
import sqlite3


conn = sqlite3.connect('data/League.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS test3 (summonerID, role, season, champion, lane);")
conn.commit()

#Gunna need to update this everyday, fun
API_KEY = "RGAPI-ee771521-37c9-4c27-b826-2e6ae442a45c"

CHALLENGER_LEAGUE = "https://na1.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + API_KEY

def main():

	ma = grab_challenger_matches()
	print ma
	insert_matches_to_db(ma)
	


	#close connection to sqlite
	conn.close();


def grab_challenger_matches():
	#Get summoner IDs from challenger league
	url = CHALLENGER_LEAGUE

	response = urllib.urlopen(url)
	dontgetbanned(response)
	data = json.loads(response.read())
	entries = data["entries"]

	matches = []
	for rows in range (len(entries)):
		try:
			summonerID = entries[rows]['playerOrTeamId']
		except Keyerror, e:
			print entries
			summonerID = "-1"
			print "Keyerror " + str(e)
		#Replace name with a questionmark if it cant be encoded, koreans playing this game reeeeee
		#This is actually useless, not gunna put it into db because I dont think its worth fixing all the potential errors with people using random characters
		#and sqlite doenst like all types of encoding
		#######playerName = entries[rows]['playerOrTeamName'].encode(sys.stdout.encoding, errors = 'replace')

		#PlayerID to accountID conversion
		playerID = summonerID_TOaccountID(summonerID)
		#print playerID

		#After you hvae the ID's get their match history
		ACCOUNT_MATCH_LIST = "https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/"+str(playerID)+"?api_key="+API_KEY

		url = ACCOUNT_MATCH_LIST
		response = urllib.urlopen(url)
		dontgetbanned(response)
		data = json.loads(response.read())
		matches= matches + data["matches"]
	return matches

def insert_matches_to_db(matches):
	for rows in range (len(matches)):
		try:
			role = matches[rows]['role']
			season = matches[rows]['season']
			champion = matches[rows]['champion']
			lane = matches[rows]['lane']

			#shove data into sqlite
			c.execute("INSERT INTO test3 VALUES (?,?,?,?,?);", ("1234", role, season, champion, lane))
			conn.commit()
		except KeyError, e:
			##print matches
			print "Keyerror " + str(e)
			role = "-1"
			season = "-1"
			champion = "-1"
			lane = "-1"


#Returns account ID from a known summoner ID
def summonerID_TOaccountID(summonerID):
	try:
		SUMMONER_V3 = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/" + summonerID + "?api_key=" + API_KEY
		url = SUMMONER_V3
		response = urllib.urlopen(url)
		dontgetbanned(response)
		data = json.loads(response.read())
		summonerdata = data
		playerID = summonerdata["accountId"]
		return playerID
	except KeyError, e:
		print summonerdata
		print "Keyerror " + str(e)
		return -1

#Rate limiter, stops the program if a rate goes above the league rate
#Should make it pause instead of stop, too lazy atm
def dontgetbanned(response):
	#Gets data from league API headers, contains limit and how much youve used
	curAppCount = response.info().getheader('X-App-Rate-Limit-Count')
	curAppLimit = response.info().getheader('X-App-Rate-Limit')
	x = curAppCount.split(',')
	RequestsPerSecond = x[1].split(':')
	x = curAppLimit.split(',')
	MaxRequestsPerSecond = x[1].split(':')
	if(int(RequestsPerSecond[0])>int(MaxRequestsPerSecond[0])):
		sys.exit("Rate too high")





if __name__ == '__main__':
	main()
