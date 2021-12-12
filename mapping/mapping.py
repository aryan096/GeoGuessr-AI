import numpy as np
import h5py
from global_land_mask import globe
import requests
import matplotlib.pyplot as plt
from mapping.keys import API_KEY
from mapping.keys import API_KEY_2
import json 
import google_streetview.api
from PIL import Image

min_lat, max_lat = 35, 75 #40
min_lon, max_lon = -24, 50 #74
num_loc_per_cell = 10

def single_request_meta(lat, lon):
	r = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location={lat},{lon}&radius=250&key={API_KEY}&source=outdoor')
	r = r.json()
	if r['status'] != "OK":
		print("Something went wrong...")
		return None
	return r['pano_id']

#Takes in lat, lon and returns a single pano image
# Used for getting single image for classification
def external_single_request(lat, lon):
	pano = single_request_meta(lat, lon)
	images = []
	for i in range(4):
		params = [{
		'size': '640x640', # max 640x640 pixels
		'pano': pano,
		'heading': str(90*i),
		'key': API_KEY_2
		}]
		results = google_streetview.api.results(params)
		results.download_links('temp')
		images.append(np.asarray(Image.open('temp/gsv_0.jpg')))
	
	t = np.concatenate((images[0], images[1], images[2], images[3]), axis=1)
	img = Image.fromarray(t)
	return img

def save_h5(name, data):
	with h5py.File(name+'.h5', 'w') as hf:
		hf.create_dataset("dataset_1",  data=data)

def open_h5(name):
	with h5py.File(name+'.h5', 'r') as hf:
		data = hf['dataset_1'][:]
	return data	

# IF run, will generate random coordinates everywhere, then will make streetview metadata requests to see if streetview is availble there
# Will overwrite previous data!
def generate_all_coords():
	arr = np.empty([40, 74, num_loc_per_cell, 2])
	id_dic = {}
	for i in range(arr.shape[0]):
		for j in range(arr.shape[1]):
			arr[i,j,:,0] = np.around(np.random.uniform(low=i+35, high=i+35+1, size=num_loc_per_cell), 6)
			arr[i,j,:,1] = np.around(np.random.uniform(low=j-24, high=j-24+1, size=num_loc_per_cell), 6)


	for i in range(arr.shape[0]):
		#print(i)
		for j in range(arr.shape[1]):
			for k in range(num_loc_per_cell):
				if globe.is_land(arr[i,j,k,0], arr[i,j,k,1]) == False:
					arr[i,j,k,0] = None
					arr[i,j,k,1] = None
					continue
				lat = arr[i,j,k,0]
				lon = arr[i,j,k,1]
				response = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location={lat},{lon}&radius=25000&key={API_KEY}&source=outdoor')
				r = response.json()
				if r['status'] != "OK":
					arr[i,j,k,0] = None
					arr[i,j,k,1] = None
					continue
				#print(r)
				if r['pano_id'] not in id_dic:
					id_dic[r['pano_id']] = r['location']
	save_h5('np_data2', arr)
	with open("pano_ids.json", "w") as outfile:
		json.dump(id_dic, outfile)
	return arr, id_dic

#Reads the current list of pano images and locations and plots them on a map
def plot_streetview_locs():
	with open('pano_ids.json') as json_file:
		pano_ids = json.load(json_file)
	x = []
	y = []
	for pano in pano_ids:
		x.append(pano_ids[pano]['lng'])
		y.append(pano_ids[pano]['lat'])
	plt.plot(x, y, 'bo', markersize=0.5)
	plt.show()

# DO NOT RUN UNLESS ABSOLUTELY SURE
# Downloads all pano images listed in pano_ids.json
def download_all_images():
	with open('pano_ids.json') as json_file:
		pano_ids = json.load(json_file)

	for pano in list(pano_ids.keys()):
		images = []
		for i in range(4):
			params = [{
			'size': '640x640', # max 640x640 pixels
			'pano': pano,
			'heading': str(90*i),
			'key': API_KEY_2
			}]
			results = google_streetview.api.results(params)
			results.download_links('temp')
			images.append(np.asarray(Image.open('temp/gsv_0.jpg')))
		
		t = np.concatenate((images[0], images[1], images[2], images[3]), axis=1)
		i = Image.fromarray(t)
		i.save("images/"+str(pano)+".jpg")