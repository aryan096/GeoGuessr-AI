import os
import hyperparameters as hp
from model import GeoLocationCNN
import tensorflow as tf
import numpy as np
from PIL import Image
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import colors
import json

class Classifier():
    def __init__(self):
        #print(os.path.dirname(os.path.realpath(__file__)))
        self.model = GeoLocationCNN()
        self.model(tf.keras.Input(shape=(1280, 320, 3)))
        self.model.vgg16.load_weights('vgg16_imagenet.h5', by_name=True)
        self.model.head.load_weights('current weights/vgg.weights.e041-acc0.0575.h5', by_name=False)
        self.predictions = None

    def classify(self, image):
        if type(image) == str:
            with Image.open(image) as im:
                img = im
        else:
            img = image
        img = img.resize((1280, 320))
        img = np.asarray(img)/255
        img = np.expand_dims(img, axis=0)
        #mean, std = np.mean(img, axis=(0,1,2)), np.std(img, axis=(0,1,2))
        #img = (img - mean) / std
        self.predictions = self.model.predict(img).squeeze()

    # Creates and opens a heatmap based on current predictions
    def visualize_map(self):
        if self.predictions is None:
            raise Exception("No predictions to visualize")

        def gen_color(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
            c1=np.array(colors.to_rgb(c1))
            c2=np.array(colors.to_rgb(c2))
            return colors.to_hex((1-mix)*c1 + mix*c2)
        def gen_color_fade(c1,c2,n):
            c = []
            for i in range(n):
                c.append(gen_color(c1, c2, i/n))
            return c    

        def find_cell_coords(map,lat,lon):
            lat = lat*5
            lon = lon*5
            lats = [lat, lat, lat+5, lat+5]
            lons = [lon, lon+5, lon+5, lon]
            for i in range(4):
                lons[i], lats[i] = map(lons[i], lats[i])
            #print(lats, lons)
            return lats, lons

        with open("idx_to_class.json", "r") as file:
            idx_to_class = json.load(file)

        # Generates list of heatmap colors
        colors_list = gen_color_fade('red', 'blue', 89)

        map = Basemap(projection='mill', resolution = 'l', area_thresh = 100, llcrnrlon=-24, llcrnrlat=35,urcrnrlon=50, urcrnrlat=75)
        map.drawcoastlines()
        map.drawcountries()
        map.drawmeridians(np.arange(-20, 50, 5))
        map.drawparallels(np.arange(35, 75, 5))
        
        # For each output of model classifier, plots it on map coorsponding to 
        for i in range(self.predictions.shape[0]):
            class_name = idx_to_class[str(i)]

            nums = class_name.split("lon")
            nums[0] = nums[0][3:]
     
            lat, lon = int(float(nums[0])), int(float(nums[1]))
            lats, lons = find_cell_coords(map, lat, lon)
            idx = np.argsort(self.predictions)

            colors_list = [colors_list[i] for i in idx]
            plt.fill_between(lons, lats, color=colors_list[i], edgecolor=(0,0,0,0))

        plt.show()       