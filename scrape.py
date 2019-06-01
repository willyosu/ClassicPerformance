import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Function to get data from osustats.ppy.sh since APIv2 is not ready yet.
# Unreliable for now, but it's the best set we have we have to estimate a user's performance.
# Function to get data from osustats.ppy.sh
def getData(Player):
	# Takes date and return the number of days since (Y-M-D format)
	def daysSince(desiredDate):
		desiredDate = datetime.datetime.strptime(desiredDate, "%Y-%m-%d")
		currentDate = datetime.datetime.today()
		delta = currentDate - desiredDate
		return delta.days
	
	# Creating arrays for storing the data
	Ranks = []
	Dates = []
	Performances = []
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
		
		RankData = driver.find_elements_by_class_name("rank")
		DateData = driver.find_elements_by_class_name("date")
		PerformanceData = driver.find_elements_by_class_name("pp")
		nonlocal endOfResults
		
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
		# Adding pp data to array
		for i in PerformanceData:
			i = i.text
			remove = "-"
			for character in remove:
				i = i.replace(character, "0")
			try:
				i = int(i)
			except:
				pass
			else:
				Performances.append(i)
	for i in range(1, int(Pages) + 1):
		Page(str(i))
		if (endOfResults) or (i == int(Pages)):
			Scores = []
			for j in range(len(Dates)):
				Scores.append(tuple((Ranks[j], Dates[j], Performances[j])))
			return(Scores)
		else:
			pass
	driver.close()
