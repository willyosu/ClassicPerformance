import ClassicPerformance as cpp

# Calculating a single play
# args: Rank, Accuracy, Mods, Age, Difficulty, Popularity
singlePP = cpp.calcPlay(1, 99.83, 1.075, 983, 7.29, 209348)

# Getting performace from the user 'Cookiezi' via webscrape
scrapePP = cpp.scrapePerformance("Cookiezi")

# Calculating total from score array of 2 scores
userScores = [[1, 99.83, 1.075, 983, 7.29, 209348],[3, 97.33, 1.125, 381, 5.65, 36859]]
calcPP = cpp.classicPerformance(userScores)

print("Single play pp: " + str(singlePP))
print("Scraped pp: " + str(scrapePP))
print("Calculated pp: " + str(calcPP))
