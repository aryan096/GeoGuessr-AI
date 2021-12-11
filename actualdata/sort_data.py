import numpy as np
import h5py
#from global_land_mask import globe
#import requests
import matplotlib.pyplot as plt
#from keys import API_KEY
import json 
import shutil
import os
import random

min_lat, max_lat = 35, 75 #40
min_lon, max_lon = -24, 50
num_pixels_in_class = 5
train_size = 0.8

with open('../mapping/pano_ids.json') as json_file:
	imagelatlongs = json.load(json_file)

os.mkdir("train")
os.mkdir("test")

counter = 0
items = list(imagelatlongs.items())
for i in range(1000):
	random.shuffle(items)
for item in items:
	coords = item[1]
	lat = coords["lat"]
	lon = coords["lng"]
	latclass = str(lat // num_pixels_in_class)
	lonclass = str(lon // num_pixels_in_class)
	img_name = item[0]
	dirname = "lat" + latclass + "lon" + lonclass
	if counter < train_size * len(imagelatlongs.items()): #train data
		try:
			os.mkdir("train/" + dirname) # create directory for class
			shutil.copy2("imageziphere/images/" + item[0] + ".jpg", "train/" + dirname)
		except: #means that directory for class already exists
			shutil.copy2("imageziphere/images/" + item[0] + ".jpg", "train/" + dirname)
	else: #test data
		try:
			os.mkdir("test/" + dirname) # create directory for class
			shutil.copy2("imageziphere/images/" + item[0] + ".jpg", "test/" + dirname)
		except: #means that directory for class already exists
			shutil.copy2("imageziphere/images/" + item[0] + ".jpg", "test/" + dirname)
	counter += 1

print(len(imagelatlongs.items()), "sorted into grid squares and separated into train and test data")
