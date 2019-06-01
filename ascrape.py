import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Function to get data from osustats.ppy.sh since APIv2 is not ready yet.
# Unreliable for now, but it's the best set we have we have to estimate a user's performance.
def get(Player):
	# Takes date and return the number of days since (Y-M-D format)
	def Since(Date_Play):
		Date_Play = datetime.datetime.strptime(Date_Play, "%Y-%m-%d")
		Date_Current = datetime.datetime.today()
		delta = Date_Current - Date_Play
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
	def Page(Page_Number):
		driver.get("https://osustats.ppy.sh/u/" + Player + "//" + Page_Number + "//2////1-500/")
		element_present = expected_conditions.presence_of_element_located((By.XPATH, """/html/body/div/div/div/div[2]/div[1]/div/div[1]"""))
		WebDriverWait(driver, 5).until(element_present)
		
		Rank_Data = driver.find_elements_by_class_name("rank")
		Date_Data = driver.find_elements_by_class_name("date")
		Performance_Data = driver.find_elements_by_class_name("pp")
		nonlocal endOfResults
		
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
		# Checking date data and adding to array
		for i in Date_Data:
			i = i.text
			try:
				Since(i)
			except:
				pass
			else:
				Dates.append(Since(i))
		# Adding pp data to array
		for i in Performance_Data:
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
