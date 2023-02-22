import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import FastMarkerCluster

#Geospatial data manipulation
import pandas as pd
import geopandas as gpd
import numpy as np
#Used for working with geometrical figures 
from shapely.geometry import Point
#Used for geospatial visualization


canadian_cities = pd.read_csv(r"canadacities.csv")

geometry_cities = [ Point(xy) for xy in zip(canadian_cities["lng"],canadian_cities["lat"])   ]

gdf = gpd.GeoDataFrame(canadian_cities,crs="EPSG:4326",geometry=geometry_cities)

#mean for canada
gdf_mean_lat = np.mean(gdf.lat)
gdf_mean_lng = np.mean(gdf.lng)

ns_lat = 44.6923
ns_lng = -62.6572


my_map = folium.Map(location=[ns_lat,ns_lng], zoom_start=7)
#folium.GeoJson(data = gdf).add_to(my_map)
my_map.add_child(FastMarkerCluster(gdf[["lat","lng"]].values.tolist()))

st.title("Clustering Canadian Cities", anchor=None)

st_data = st_folium(my_map,width=1000)


values = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

