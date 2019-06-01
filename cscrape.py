import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Function to get data from osustats.ppy.sh since APIv2 is not ready yet.
# Unreliable for now, but it's the best set we have we have to estimate a user's performance.
def get(Player, Age_Falloff):
	# Takes date and return the number of days since (Y-M-D format)
	def Since(Date_Play):
		Date_Play = datetime.datetime.strptime(Date_Play, "%Y-%m-%d")
		Date_Current = datetime.datetime.today()
		delta = Date_Current - Date_Play
		return delta.days
	
	# Creating arrays for storing the data
	Links = []
	Ranks = []
	Hits = []
	Misses = []
	Accuracies = []
	ModCombo = []
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
	def Page(Page_Number):
		driver.get("https://osustats.ppy.sh/u/" + Player + "//" + Page_Number + "//2////1-500/")
		element_present = expected_conditions.presence_of_element_located((By.XPATH, """/html/body/div/div/div/div[2]/div[1]/div/div[1]"""))
		WebDriverWait(driver, 5).until(element_present)
		
		Beatmap_Data = driver.find_elements_by_css_selector("div.beatmapInfo > div > a")
		Rank_Data = driver.find_elements_by_class_name("rank")
		Hit_Data = driver.find_elements_by_class_name("hits")
		Miss_Data = driver.find_elements_by_class_name("misses")
		ModCombo_Data = driver.find_elements_by_class_name("mods")
		Date_Data = driver.find_elements_by_class_name("date")
		nonlocal endOfResults
		nonlocal Age_Falloff
		
		# Getting links to each beatmap page
		for i in Beatmap_Data:
			i = i.get_attribute("href")
			Links.append(i)
		
		# Converting rank data to numbers and adding to array
		for i in Rank_Data:
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
		for i in Hit_Data:
			Hits.append(i.text)
		
		# Adding miss data to array
		for i in Miss_Data:
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
		for i in ModCombo_Data:
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
				ModCombo.append(modSum)
		
		# Checking date data and adding to array
		for i in Date_Data:
			i = i.text
			try:
				Since(i)
			except:
				pass
			else:
				if Since(i) > Age_Falloff:
					endOfResults = True
					pass
				else:
					Dates.append(Since(i))
		
		# Fetching difficulty and popularity data from each beatmap
		for i in Links:
			driver.get(i)
			Difficulty_Data = driver.find_element_by_css_selector("table.beatmap-stats-table > tbody > tr:last-child > td.beatmap-stats-table__value")
			Popularity_Data = driver.find_element_by_class_name("beatmap-success-rate__percentage")
			Popularity_Data = Popularity_Data.get_property("title")
			Popularity_Data = Popularity_Data.split(" / ")
			PopularityString = Popularity_Data[0].replace(",","")
			Difficulties.append(float(Difficulty_Data.text))
			Popularities.append(int(PopularityString))
		
	for i in range(1, int(Pages) + 1):
		Page(str(i))
		if (endOfResults) or (i == int(Pages)):
			Scores = []
			for j in range(len(Dates)):
				Scores.append(tuple((Ranks[j], Accuracies[j], ModCombo[j], Dates[j], Difficulties[j], Popularities[j])))
			return(Scores)
		else:
			pass
	driver.close()