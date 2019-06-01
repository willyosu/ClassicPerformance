import ActivePerformance as app

# Calculating a single play
# args: Rank, Accuracy, Mods, Age, Difficulty, Popularity
singlePP = app.calcPlay(1, 983, 896)

# Getting performace from the user 'Cookiezi' via webscrape
scrapePP = app.scrapePerformance("Cookiezi")

# Calculating total from score array of 2 scores
userScores = [[1, 99.83, 1.075, 983, 7.29, 209348],[3, 97.33, 1.125, 381, 5.65, 36859]]
calcPP = app.activePerformance(userScores)

print("Single play pp: " + str(singlePP))
print("Scraped pp: " + str(scrapePP))
print("Calculated pp: " + str(calcPP))

# File print the performance total for the user 'Cookiezi' via webscrape
ap = ("ap:" + str("{:,}".format(round(app.scrapePerformance("Cookiezi")))))
with open('ap.txt', 'w') as f:
  print(ap, file=f)
