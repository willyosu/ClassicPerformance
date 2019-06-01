import math
import scrape

# Global variables
Player = "Username"
Age_Falloff = 365
Popularity_Falloff = 100000
Rank_Falloff = 500

# Rank: play's position on leaderboard
# Accuracy: accuracy of the play (between 0.00 and 100.00)
# Age: number of days since play was set
# Difficulty: map's star rating
# Popularity: total number of ranked plays on the map (NOT playcount)
def play(Rank, Accuracy, Mods, Age, Difficulty, Popularity):
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

def weight(performanceArray):
	# Takes array of performances and weights and calculates total performance
	performanceArray.sort(reverse=True)
	for i in range(len(performanceArray)):
		performanceArray[i] = performanceArray[i]*((0.95)**i)
	return sum(performanceArray)

# Calculate performance from an array of array constructed as follows: scoreArray[i][Rank, Accuracy, Mods, Age, Difficulty, Popularity]
def calc(scoreArray):
	Totals = []
	for i in range(len(scoreArray)):
		Totals.append(play(scoreArray[i][0], scoreArray[i][1], scoreArray[i][2], scoreArray[i][3], scoreArray[i][4], scoreArray[i][5]))
	return weight(Totals)

# Calculate performance for a user by webscraping data using scrape.py
def scrape(User):
	userData = scrape.get(User, Age_Falloff)
	Totals = []
	for i in range(len(userData)):
		Totals.append(play(userData[i][0], userData[i][1], userData[i][2], userData[i][3], userData[i][4], userData[i][5]))
	return weight(Totals)
