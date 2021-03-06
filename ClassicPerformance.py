import math
import osustatsscraper as scraper

# Global variables/constants
Age_Falloff = 365
Popularity_Falloff = 100000
Rank_Falloff = 500

# Takes array of performances and weights and calculates total performance
def weight(performanceArray):
	performanceArray.sort(reverse=True)
	for i in range(len(performanceArray)):
		performanceArray[i] = performanceArray[i]*((0.95)**i)
	return sum(performanceArray)

# Calculate performance from an array of array constructed as follows: scoreArray[i][Rank, Age, Performance]
def acalc(scoreArray):
	Totals = []
	for i in range(len(scoreArray)):
		Totals.append(play(userData[i][0], userData[i][1], userData[i][2]))
	return weight(Totals)

# Active performance single play calculation
def aplay(Rank, Age, Performance):
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

# Calculate performance for a user by webscraping data
def ascrape(User):
	userData = scraper.aget(User)
	Totals = []
	for i in range(len(userData)):
		Totals.append(aplay(userData[i][0], userData[i][1], userData[i][2]))
	return weight(Totals)

# Classic performance single play calculation
def cplay(Rank, Accuracy, Mods, Age, Difficulty, Popularity):
	# Determines age falloff
	if Age >= Age_Falloff:
		Age_Factor = 0.01
	else:
		Age_Factor = math.log(-1 * Age + (Age_Falloff + 1), Age_Falloff + 1) + 0.01
	
	# Determines popularity factor based on number of ranked plays
	Popularity_Factor = math.log(Popularity, Popularity_Falloff)
	
	# Determines rank falloff
	if Rank >= Rank_Falloff:
		Rank_Factor = 0.01
	else:
		Rank_Factor = (-1 * math.log(Rank, Rank_Falloff) + 1) + 0.01
		
	return (Difficulty*Accuracy*Mods*Age_Factor*Popularity_Factor*Rank_Factor)

# Calculate performance from an array of array constructed as follows: scoreArray[i][Rank, Accuracy, Mods, Age, Difficulty, Popularity]
def ccalc(scoreArray):
	Totals = []
	for i in range(len(scoreArray)):
		Totals.append(play(scoreArray[i][0], scoreArray[i][1], scoreArray[i][2], scoreArray[i][3], scoreArray[i][4], scoreArray[i][5]))
	return weight(Totals)

# Calculate performance for a user by webscraping data
def cscrape(User):
	userData = scraper.cget(User, Age_Falloff)
	Totals = []
	for i in range(len(userData)):
		Totals.append(cplay(userData[i][0], userData[i][1], userData[i][2], userData[i][3], userData[i][4], userData[i][5]))
	return weight(Totals)
