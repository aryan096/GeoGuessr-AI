import pandas as pd 
import numpy as np
import pycristoforo as pyc
import requests 
import json

LOCATIONS_PER_COUNTRY = 100
RADIUS = 1000000
API_KEY = 'AIzaSyBW_KfI1Qw_CKjcvTJDuWTMDywpEGNfmGI'

# get list of european countries
countries = pd.read_csv('europe_countries.csv')
countries = list(countries['name'])

# 1. iterate through country list 
# 2. for each country, get LOCATIONS_PER_COUNTRY locations for that country using pycristoforo
# 3. iterate through each location, make street view metadata call with RADIUS radius

pano_ids = {}

for country in countries:

    try:
        country_shape = pyc.get_shape(country)
        points = pyc.geoloc_generation(country_shape, LOCATIONS_PER_COUNTRY, country)
    except:
        print(country, ' not found')
        continue

    country_pano_ids = []

    for i, point in enumerate(points):
        print(country, i)
        lat = point['geometry']['coordinates'][0]
        longit = point['geometry']['coordinates'][1]

        # make API call
        response = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location={lat},{longit}&radius={RADIUS}&key={API_KEY}')
        try:
            country_pano_ids.append(response.json()['pano_id'])
        except:
            print(response.json())
            print('no coordinate found :(')
    
    pano_ids[country] = country_pano_ids

with open("europe_pano_100_40000.json", "w") as outfile:
    json.dump(pano_ids, outfile)
# pyc.geoloc_print(points, ',')