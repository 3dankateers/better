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
import simplejson
#bypass cloudflare with requests, its better than urllib
import requests

conn = sqlite3.connect('data/TournamentData.sqlite')
c = conn.cursor()

####37 values, 1 of them is date
c.execute("CREATE TABLE IF NOT EXISTS TournamentDataRaw (gameId, platformId, gameDuration, seasonId, gameVersion, champ1, champ2, champ3, champ4, champ5, champ6, champ7, champ8, \
	champ9, champ10, player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, ban1, ban2, ban3, ban4, ban5, ban6, ban7, ban8, ban9, ban10, winningTeam, datePulled);")

conn.commit()


LEAGUE_API_HTTPS = "https://acs.leagueoflegends.com/v1/stats/game/"
platformIdURL = "TRLH3/"
gameIdURL = "1002300059?"
gameHash = "gameHash=5b203758165709fc"

def main():
	url = LEAGUE_API_HTTPS + platformIdURL + gameIdURL + gameHash


	getScheduleItemsFromLeagueID(9)


	#getTournamentCodesFromLeagueID(9)

	#insertTournamentMatch(url)

def insertTournamentMatch(url):
	#initialize some lists
	gameId = []
	platformId = []
	gameDuration = []
	seasonId = []
	gameVersion = []
	champ = []
	player = []
	ban = []
	winningTeam = []

	response = urllib.urlopen(url)
	data = json.loads(response.read())

	gameId = (data['gameId'])
	platformId = (data['platformId'])
	gameDuration = (data['gameDuration'])
	seasonId = (data['seasonId'])
	gameVersion = (data['gameVersion'])

	for i in range(0,10):
		champ.append(data['participants'][i]['championId'])
		player.append(data['participantIdentities'][i]['player']['summonerName'])

	for x in range(0,2):
		for i in range(0,5):
			ban.append(data['teams'][x]['bans'][i]['championId'])

	if(data['teams'][0]['win']=="Win"):
		winningTeam = 100
	else:
		winningTeam = 200

	c.execute("INSERT OR IGNORE INTO TournamentDataRaw VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now','localtime'));", (gameId, platformId,\
		gameDuration, seasonId, gameVersion, champ[0], champ[1], champ[2], champ[3], champ[4], champ[5], champ[6], champ[7], champ[8], champ[9], player[0], player[1], player[2], player[3],\
		player[4], player[5], player[6], player[7], player[8],player[9], ban[0], ban[1], ban[2], ban[3], ban[4], ban[5], ban[6], ban[7], ban[8], ban[9], winningTeam))

	conn.commit()
	conn.close()	

def getTournamentCodesFromLeagueID(LeagueID):
	url = "http://api.lolesports.com/api/v1/leagues?id="+str(LeagueID)
	###Using requests library to bypass cloudflare
	response = requests.get(url)
	data = json.loads(response.content)
	tournamentCodes = []
	tournamentCodes = (data['leagues'][0]['tournaments'])

	for i in range(len(data['leagues'])-1):
		for x in range(len(data['leagues'][i]['tournaments'])):
			tournamentCodes.append((data['leagues'][i]['tournaments'][x]))

	return tournamentCodes

def getScheduleItemsFromLeagueID(LeagueID):
	url = "http://api.lolesports.com/api/v1/scheduleItems?leagueId=" + str(LeagueID)

	response = requests.get(url)
	data = json.loads(response.content)

	cancerIterator = 0

	matchId = []
	tournamentId = []
	platformId = []
	gameId = []
	tournamentName = []

	for i in range(len(data['highlanderTournaments'])):
		for x in range(len(data['highlanderTournaments'][i]['platformIds'])):
			try:
				PlatformAndGame = data['highlanderTournaments'][i]['platformIds'][x]
				temp = PlatformAndGame.split(':')
				platformId.append(temp[0])
				gameId.append(temp[1])
				tournamentId.append(data['highlanderTournaments'][i]['id'])
				tournamentName.append(data['highlanderTournaments'][i]['title'])
				matchId.append(data['scheduleItems'][cancerIterator]['match'])
			except KeyError as e:
				print "Invalid Key on position " + str(cancerIterator) + " called " + str(e)
			except:
				print "Catchall"

			cancerIterator+=1


	schedule = zip(platformId, gameId, tournamentId, tournamentName, matchId)

	return schedule

def ScheduleToGameID(schedule):
	matchId, tournamentId = schedule

	url = "http://api.lolesports.com/api/v2/highlanderMatchDetails?tournamentId=" + tournamentId + "&matchId=" + matchId

	response = requests.get(url)
	data = json.loads(response.content)



if __name__ == '__main__':
	main()