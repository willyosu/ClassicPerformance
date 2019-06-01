import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

# Function to get data from osustats.ppy.sh since APIv2 is not ready yet.
# Unreliable for now, but it's the best set we have we have to estimate a user's performance.
def get(Player):
	# Takes date and return the number of days since (Y-M-D format)
	def Since(dateOfPlay):
		dateOfPlay = datetime.datetime.strptime(dateOfPlay, "%Y-%m-%d")
		dateOfToday = datetime.datetime.today()
		delta = dateOfToday - dateOfPlay
		return delta.days
	
	# Creating arrays for storing the data
	arrayOfRanks = []
	arrayOfDates = []
	arrayOfPerformances = []
	endOfResults = False
	
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get("https://osustats.ppy.sh/u/" + Player + "//1//2////1-500/")
	WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, """//*[@id="line-chart"]""")))
	Pages = driver.find_element_by_xpath("""/html/body/div/div/div/div[2]/div[1]/div/div[1]""").get_attribute("textContent")
	Pages = Pages.replace(" ","").split("of")
	numOfPages = Pages[-1]
	
	# Creating webdriver to fetch data
	def Page(Page_Number):
		driver.get("https://osustats.ppy.sh/u/" + Player + "//" + Page_Number + "//2////1-500/")
		WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, """//*[@id="line-chart"]""")))
		
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
				arrayOfRanks.append(i)
		
		# Checking date data and adding to array
		for i in Date_Data:
			i = i.text
			try:
				Since(i)
			except:
				pass
			else:
				arrayOfDates.append(Since(i))
		
		# Fetching difficulty and popularity data from each beatmap
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
				arrayOfPerformances.append(i)
		
	for i in range(1, int(numOfPages) + 1):
		Page(str(i))
		if (endOfResults) or (i == int(numOfPages)):
			Scores = []
			for j in range(len(arrayOfDates)):
				Scores.append(tuple((arrayOfRanks[j], arrayOfDates[j], arrayOfPerformances[j])))
			return(Scores)
		else:
			pass
	driver.close()
