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

conn = sqlite3.connect('data/Summoners.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS SummonersList (summonerID, accountID, tier, region, rank, leaguePoints, queueType, dateScraped);")
conn.commit()

CHALLENGER_LEAGUE = "https://na1.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + API_KEY
MASTERS_LEAGUE = "https://na1.api.riotgames.com/lol/league/v3/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + API_KEY

def main():

	#use this if you want some other league
	LEAGUE_UUID = ""
	RANDOM_LEAGUE = "https://na1.api.riotgames.com/lol/league/v3/leagues/" + LEAGUE_UUID +"?api_key=" + API_KEY

	insertIntoDB(pullSummonersFromURL(CHALLENGER_LEAGUE))
	#insertIntoDB(pullSummonersFromURL(MASTERS_LEAGUE))

	#close connection to sqlite
	conn.close();

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
		dump_to_file(summonerdata)
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
	RequestsPerMinute = x[0].split(':')
	x = curAppLimit.split(',')
	MaxRequestsPerSecond = x[1].split(':')
	MaxRequestsPerMinute = x[0].split(':')

	#its actually per 2 minutes
	if(int(RequestsPerMinute[0])>(int(MaxRequestsPerMinute[0])-3)):
		print "Rate too high"
		time.sleep(110)

	if(int(RequestsPerSecond[0])>(int(MaxRequestsPerSecond[0])-2)):
		print "Rate too high"
		time.sleep(5)

def dump_to_file(dump):
	with open("Dump.txt", 'w') as outfile:
		json.dump(dump, outfile)


def logging(insert):
	#opening with "a" for appending instead of "w" for overwrite
	logFile = open("log.txt","a")
	logFile.write(insert + "\n")
	logFile.close()

def pullSummonersFromURL(url):
	summonerID = []
	playerID = []
	league = []
	regionList = []
	rank = []
	leaguePoints = []
	queueList = []

	region = "NOT DETECTED"
	queueType = "NOT DETECTED"

	response = urllib.urlopen(url)
	dontgetbanned(response)
	data = json.loads(response.read())

	if "na1" in url:
		region = "NA1"

	if "RANKED_SOLO_5x5" in url:
		queueType = "RANKED SOLO 5x5"



	entries = data["entries"]
	for rows in range (len(entries)):
		summonerID.append(entries[rows]['playerOrTeamId'])
		playerID.append(summonerID_TOaccountID(summonerID[rows]))
		league.append(data["tier"])
		regionList.append(region)
		rank.append(entries[rows]['rank'])
		leaguePoints.append(entries[rows]['leaguePoints'])
		queueList.append(queueType)



	#combine lists into a tuple
	databaseInsert = zip(summonerID,playerID,league,regionList,rank,leaguePoints,queueList)
	return databaseInsert

def insertIntoDB(tupleInsert):
	c.executemany("INSERT OR IGNORE INTO SummonersList VALUES (?,?,?,?,?,?,?,datetime('now','localtime'));", (tupleInsert))
	conn.commit()
	conn.close()

if __name__ == '__main__':
	main()
