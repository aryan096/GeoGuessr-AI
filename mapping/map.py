import numpy as np
import h5py
from global_land_mask import globe
import requests
import matplotlib.pyplot as plt
from keys import API_KEY

min_lat, max_lat = 35, 75 #40
min_lon, max_lon = -24, 50 #74
num_loc_per_cell = 10

def save_h5(name, data):
	with h5py.File(name+'.h5', 'w') as hf:
		hf.create_dataset("dataset_1",  data=data)

def generate_all_coords():
	arr = np.empty([40, 74, num_loc_per_cell, 2])
	id_dic = {}
	for i in range(arr.shape[0]):
		for j in range(arr.shape[1]):
			arr[i,j,:,0] = np.around(np.random.uniform(low=i+35, high=i+35+1, size=num_loc_per_cell), 6)
			arr[i,j,:,1] = np.around(np.random.uniform(low=j-24, high=j-24+1, size=num_loc_per_cell), 6)

	#print(arr[10,10,2,:])	

	for i in range(arr.shape[0]):
		print(i)
		for j in range(arr.shape[1]):
			for k in range(num_loc_per_cell):
				if globe.is_land(arr[i,j,k,0], arr[i,j,k,1]) == False:
					arr[i,j,k,0] = None
					arr[i,j,k,1] = None
					continue
				lat = arr[i,j,k,0]
				lon = arr[i,j,k,1]
				response = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location={lat},{lon}&radius=5000&key={API_KEY}')
				r = response.json()
				if r['status'] != "OK":
					arr[i,j,k,0] = None
					arr[i,j,k,1] = None
					continue
				print(r)
				if r['pano_id'] not in id_dic:
					id_dic['pano_id'] = r['location']
	save_h5('np_data', arr)
	with open("pano_ids.json", "w") as outfile:
		json.dump(id_dic, outfile)
	return arr, id_dic



def open_h5(name):
	with h5py.File(name+'.h5', 'r') as hf:
		data = hf['dataset_1'][:]
	return data	

def plot(arr):
	x = arr[:,:,:,1]
	y = arr[:,:,:,0]
	plt.plot(x.flatten(),y.flatten(), 'bo', markersize=0.5)
	plt.show()

#arr, id_dic = generate_all_coords()
arr = open_h5("np_data")
#print(arr[39, 43, : ,:])
print(np.count_nonzero(~np.isnan(arr.flatten())))
plot(arr)
s = 0
for i in range(arr.shape[0]):
	for j in range(arr.shape[1]):
		if np.count_nonzero(~np.isnan(arr[i,j,:,:])) > 0:
			s += 1
print(s)	
#response = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location=74.37783861,19.16929152&radius=5000&key={API_KEY}')
#r = response.json()
#print(r)
#if r['status'] != "OK":
#	print("hello")
#else:
#	print("bad")	
# g = generate_all_coords()
# save_h5("data",g)
# arr = open_h5("data")
# good = 0
# bad = 0
# for i in range(arr.shape[0]):
# 	for j in range(arr.shape[1]):
# 		if np.nansum(arr[i,j,:,:]) == 0:
# 			print(arr[i,j,:,:])
# 			bad += 1
# 		else:
# 			good += 1
# print(good,bad)				