from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import json
import time

class GeoGetter:
	def __init__(self, browser='Firefox', maap='europe'):
		if browser.lower() == "chrome":
			from selenium.webdriver.chrome.service import Service
			from webdriver_manager.chrome import ChromeDriverManager
			s = Service(ChromeDriverManager().install())
			self.driver = webdriver.Chrome(service=s)
		else:	
			from selenium.webdriver.firefox.service import Service
			from webdriver_manager.firefox import GeckoDriverManager
			capabilities = DesiredCapabilities.FIREFOX
			capabilities["marionette"] = True
			s = Service(GeckoDriverManager().install())
			self.driver = webdriver.Firefox(service=s, capabilities=capabilities)

		if maap.lower() == "europe":
			self.driver.get("https://www.geoguessr.com/maps/5e14c87e328e461f949ae510")
		else:
			assert(False, "Map not supported")

	def get_coordinates(self):
		# time.sleep(2)
		# self.driver.refresh()
		# time.sleep(2)
		
		j = self.driver.execute_script('return JSON.parse(document.querySelectorAll("#__NEXT_DATA__")[0].text).props.pageProps.game.rounds')
		j = list(j)
		print(j)

	def quit(self):
		self.driver.quit()
#t = GeoGetter("chrome", "europe")