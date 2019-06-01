import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Function to get data from osustats.ppy.sh since APIv2 is not ready yet.
# Unreliable for now, but it's the best set we have we have to estimate a user's performance.
def getData(Player):
	# Takes date and return the number of days since (Y-M-D format)
	def daysSince(desiredDate):
		desiredDate = datetime.datetime.strptime(desiredDate, "%Y-%m-%d")
		currentDate = datetime.datetime.today()
		delta = currentDate - desiredDate
		return delta.days
	
	# Creating arrays for storing the data
	Links = []
	Ranks = []
	Hits = []
	Misses = []
	Accuracies = []
	ModCombinations = []
	Dates = []
	Difficulties = []
	Popularities = []
	endOfResults = False
	
	driver = webdriver.Chrome()
	driver.get("https://osustats.ppy.sh/u/" + Player + "//1//2////1-500/")
	element_present = expected_conditions.presence_of_element_located((By.XPATH, """/html/body/div/div/div/div[2]/div[1]/div/div[1]"""))
	WebDriverWait(driver, 5).until(element_present)
	Pages = driver.find_element_by_xpath("""/html/body/div/div/div/div[2]/div[1]/div/div[1]""").get_attribute("textContent")
	Pages.split(" of ")
	Pages = Pages[-2] + Pages[-1]
	
	# Creating webdriver to fetch data
	def Page(pageNumber):
		driver.get("https://osustats.ppy.sh/u/" + Player + "//" + pageNumber + "//2////1-500/")
		element_present = expected_conditions.presence_of_element_located((By.XPATH, """/html/body/div/div/div/div[2]/div[1]/div/div[1]"""))
		WebDriverWait(driver, 5).until(element_present)
		
		BeatmapData = driver.find_elements_by_css_selector("div.beatmapInfo > div > a")
		RankData = driver.find_elements_by_class_name("rank")
		HitData = driver.find_elements_by_class_name("hits")
		MissData = driver.find_elements_by_class_name("misses")
		ModCombinationData = driver.find_elements_by_class_name("mods")
		DateData = driver.find_elements_by_class_name("date")
		nonlocal endOfResults
		
		# Getting links to each beatmap page
		for i in BeatmapData:
			i = i.get_attribute("href")
			Links.append(i)
		
		# Converting rank data to numbers and adding to array
		for i in RankData:
			i = i.text
			remove = "~#"
			for character in remove:
				i = i.replace(character, "")
			try:
				i = int(i)
			except:
				pass
			else:
				Ranks.append(i)
		
		# Adding hit data to array
		for i in HitData:
			Hits.append(i.text)
		
		# Adding miss data to array
		for i in MissData:
			Misses.append(i.text)
		
		# Zipping hit and miss data into an array of tuples
		AccuracyData = zip(Hits, Misses)
		
		# Converting hit and miss data and calculating accuracy
		for i in AccuracyData:
			hitList = i[0].split("/")
			hitList.append(i[1])
			try:
				int(hitList[3])
			except:
				pass
			else:
				hitList = list(map(int, hitList))
				Accuracies.append((((hitList[0])+(hitList[1]*(1/3))+(hitList[2]*(1/6)))/(sum(hitList)))*100)
		
		# Mods
		for i in ModCombinationData:
			i = i.text
			modDictionary = {'None':'0.00', 'HR':'0.05', 'HD':'0.025', 'DT':'0.10', 'NC':'0.10', 'FL':'0.05', 'EZ':'-0.2', 'NF':'-0.2', 'SO':'-0.2', 'SD':'0.00', 'PF':'0.00'}
			for j, k in modDictionary.items():
				i = i.replace(j, k)
			modArray = i.split(",")
			modSum = 1
			for j in range(len(modArray)):
				try:
					modArray[j] = float(modArray[j])
				except:
					pass
				else:
					modSum += modArray[j]
			try:
				float(modArray[0])
			except:
				pass
			else:
				ModCombinations.append(modSum)
		
		# Checking date data and adding to array
		for i in DateData:
			i = i.text
			try:
				daysSince(i)
			except:
				pass
			else:
				if daysSince(i) > ageFalloff:
					endOfResults = True
					pass
				else:
					Dates.append(daysSince(i))
		
		# Fetching difficulty and popularity data from each beatmap
		for i in Links:
			driver.get(i)
			DifficultyData = driver.find_element_by_css_selector("table.beatmap-stats-table > tbody > tr:last-child > td.beatmap-stats-table__value")
			PopularityData = driver.find_element_by_class_name("beatmap-success-rate__percentage")
			PopularityData = PopularityData.get_property("title")
			PopularityData = PopularityData.split(" / ")
			PopularityString = PopularityData[0].replace(",","")
			Difficulties.append(float(DifficultyData.text))
			Popularities.append(int(PopularityString))
		
	for i in range(1, int(Pages) + 1):
		Page(str(i))
		if (endOfResults) or (i == int(Pages)):
			Scores = []
			for j in range(len(Dates)):
				Scores.append(tuple((Ranks[j], Accuracies[j], ModCombinations[j], Dates[j], Difficulties[j], Popularities[j])))
			return(Scores)
		else:
			pass
	driver.close()
