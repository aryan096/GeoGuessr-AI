import google_streetview.api
import json
import numpy as np
from PIL import Image
from keys import API_KEY

# with open('pano_ids.json') as json_file:
with open('test.json') as json_file:
	pano_ids = json.load(json_file)

for pano in pano_ids:
	images = []
	for i in range(4):
		params = [{
		'size': '640x640', # max 640x640 pixels
		'pano': pano,
		'heading': str(90*i),
		'key': API_KEY
		}]
		results = google_streetview.api.results(params)
		results.download_links('temp')
		images.append(np.asarray(Image.open('temp/gsv_0.jpg')))
	
	t = np.concatenate((images[0], images[1], images[2], images[3]), axis=1)
	i = Image.fromarray(t)
	i.save("images/"+str(pano)+".jpg")