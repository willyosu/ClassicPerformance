import math
import scrape

# Global variables
Player = "Username"
ageFalloff = 365
popularityFalloff = 100000
rankFalloff = 500

# Rank: play's position on leaderboard
# Accuracy: accuracy of the play (between 0.00 and 100.00)
# Age: number of days since play was set
# Difficulty: map's star rating
# Popularity: total number of ranked plays on the map (NOT playcount)
def calcPlay(Rank, Accuracy, Mods, Age, Difficulty, Popularity):
	# Determines age falloff
	if Age >= ageFalloff:
		ageFactor = 0.01
	else:
		ageFactor = math.log(-1*Age+(ageFalloff+1), ageFalloff+1) + 0.01
	
	# Determines popularity factor based on number of ranked plays
	popularityFactor = math.log(Popularity, popularityFalloff)
	
	# Determines rank falloff
	if Rank >= rankFalloff:
		rankFactor = 0.01
	else:
		rankFactor = -1*math.log(Rank, rankFalloff)+1 + 0.01
		
	return (Difficulty*Accuracy*Mods*ageFactor*popularityFactor*rankFactor)

def calcTotal(scoreArray):
	# Takes array of performances and weights and calculates total performance
	scoreArray.sort(reverse=True)
	for i in range(len(scoreArray)):
		scoreArray[i] = scoreArray[i]*((0.95)**i)
	return sum(scoreArray)

# Calculate performance from an array of array constructed as follows: userScoreArray[i][Rank, Accuracy, Mods, Age, Difficulty, Popularity]
def classicPerformance(userScoreArray):
	userData = userScoreArray
	Totals = []
	for i in range(len(userData)):
		Totals.append(calcPlay(userData[i][0], userData[i][1], userData[i][2], userData[i][3], userData[i][4], userData[i][5]))
	return calcTotal(Totals)

# Calculate performance for a user by webscraping data using scrape.py
def scrapePerformance(User):
	userData = scrape.getData(User)
	Totals = []
	for i in range(len(userData)):
		Totals.append(calcPlay(userData[i][0], userData[i][1], userData[i][2], userData[i][3], userData[i][4], userData[i][5]))
	return calcTotal(Totals)
