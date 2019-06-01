import math
import ascrape as scrape

# Global variables
Player = "Username"
Age_Falloff = 365
Rank_Falloff = 1000

# Rank: play's position on leaderboard
# Age: number of days since play was set
# Performance: the ppv2 value of a given play
def play(Rank, Age, Performance):
	# Determines age falloff
	if Age >= Age_Falloff:
		Age_Factor = 0.01
	else:
		Age_Factor = math.log(-1 * Age + (Age_Falloff + 1), Age_Falloff + 1) + 0.01
	
	# Determines rank falloff
	if Rank >= Rank_Falloff:
		Rank_Factor = 0.01
	else:
		Rank_Factor = (-1 * math.log(Rank, Rank_Falloff) + 1) + 0.01
	
	return (Performance*Age_Factor*Rank_Factor)

def weight(performanceArray):
	# Takes array of performances and weights and calculates total performance
	performanceArray.sort(reverse=True)
	for i in range(len(performanceArray)):
		performanceArray[i] = performanceArray[i]*((0.95)**i)
	return sum(performanceArray)

# Calculate performance from an array of array constructed as follows: scoreArray[i][Rank, Age, Performance]
def calc(scoreArray):
	Totals = []
	for i in range(len(scoreArray)):
		Totals.append(play(userData[i][0], userData[i][1], userData[i][2]))
	return weight(Totals)

# Calculate performance for a user by webscraping data using scrape.py
def scrape(User):
	userData = scrape.getData(User)
	Totals = []
	for i in range(len(userData)):
		Totals.append(play(userData[i][0], userData[i][1], userData[i][2]))
	return weight(Totals)
