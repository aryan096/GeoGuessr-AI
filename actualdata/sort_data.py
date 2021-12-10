import numpy as np
import h5py
#from global_land_mask import globe
#import requests
import matplotlib.pyplot as plt
#from keys import API_KEY
import json 
import os

min_lat, max_lat = 35, 75 #40
min_lon, max_lon = -24, 50
num_pixels_in_class = 5
train_size = 0.8

with open('../mapping/pano_ids.json') as json_file:
	imagelatlongs = json.load(json_file)

os.mkdir("train")
os.mkdir("test")

counter = 0
for item in imagelatlongs.items():
	coords = item[1]
	lat = coords["lat"]
	lon = coords["lng"]
	latclass = str(lat // num_pixels_in_class)
	lonclass = str(lon // num_pixels_in_class)
	img_name = item[0]
	if counter < train_size * len(imagelatlongs.items()): #train data
		try:
			os.mkdir("train/lat" + latclass + "lon" + lonclass) # create directory for class
			# Get image from name of image
			# Move image to directory
		except: #means that directory for class already exists
			#code to get image from name of image
			# Move image to directory
			pass
	else: #test data
		try:
			os.mkdir("est/lat" + latclass + "lon" + lonclass) # create directory for class
			# Get image from name of image
			# Move image to directory
		except: #means that directory for class already exists
			#code to get image from name of image
			# Move image to director
			pass
	counter += 1

print(len(imagelatlongs.items()))
