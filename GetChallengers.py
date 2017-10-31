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

conn = sqlite3.connect('data/Challengers.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS ChallengerLeague (summonerID, accountID);")
conn.commit()

#Gunna need to update this everyday, fun
API_KEY = "RGAPI-ee771521-37c9-4c27-b826-2e6ae442a45c"

CHALLENGER_LEAGUE = "https://na1.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + API_KEY

def main():
	#Get summoner IDs from challenger league
	url = CHALLENGER_LEAGUE

	response = urllib.urlopen(url)
	dontgetbanned(response)
	data = json.loads(response.read())

	entries = data["entries"]
	print len(entries)
	for rows in range (len(entries)):
		summonerID = entries[rows]['playerOrTeamId']
		playerID = summonerID_TOaccountID(summonerID)
		c.execute("INSERT INTO ChallengerLeague VALUES (?,?);", (summonerID, playerID))
		conn.commit()
		logging("Row " + str(rows) + " inserted into Challenger.sqlite")

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
		time.sleep(1)
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
	x = curAppLimit.split(',')
	MaxRequestsPerSecond = x[1].split(':')

	if(int(RequestsPerSecond[0])>(int(MaxRequestsPerSecond[0])/2)):
		logging("Requests are at " + int(RequestsPerSecond[0]) + "\n")
	#print "Cur Requests: " + str(RequestsPerSecond) + " Max Requests: " + str(MaxRequestsPerSecond)

	if(int(RequestsPerSecond[0])>(int(MaxRequestsPerSecond[0])-2)):
		sys.exit("Rate too high")

def dump_to_file(dump):
	with open("Dump.txt", 'w') as outfile:
		json.dump(dump, outfile)


def logging(insert):
	#opening with "a" for appending instead of "w" for overwrite
	logFile = open("log.txt","a")
	logFile.write(insert + "\n")
	logFile.close()

if __name__ == '__main__':
	main()