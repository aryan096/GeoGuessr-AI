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
			try:
				s = Service(ChromeDriverManager().install())
				self.driver = webdriver.Chrome(service=s)
			except:
				raise Exception("There was a problem loading the Chrome browser.")	
		else:

			from selenium.webdriver.firefox.service import Service
			from webdriver_manager.firefox import GeckoDriverManager
			try:
				capabilities = DesiredCapabilities.FIREFOX
				capabilities["marionette"] = True
				s = Service(GeckoDriverManager().install())
				self.driver = webdriver.Firefox(service=s, capabilities=capabilities)
			except:
				raise Exception("There was a problem loading the Chrome browser.")		

		if maap.lower() == "europe":
			self.driver.get("https://www.geoguessr.com/maps/5e14c87e328e461f949ae510")
		else:
			raise Exception("Map not supported")

	def get_coordinates(self):
		time.sleep(1)
		self.driver.refresh()
		for i in range(5):
			try:
				t = self.driver.execute_script('return JSON.parse(document.querySelectorAll("#__NEXT_DATA__")[0].text)')
				data = self.driver.execute_script('return JSON.parse(document.querySelectorAll("#__NEXT_DATA__")[0].text).props.pageProps.game.rounds')
				break
			except:
				time.sleep(1)
				continue
		try:
			data = list(data)
		except UnboundLocalError:
			raise Exception("Data could not extracted from GeoGuessr")
		
		lat = data['lat']
		lng = data['lng']
		return lat, lng

	def quit(self):
		self.driver.quit()
