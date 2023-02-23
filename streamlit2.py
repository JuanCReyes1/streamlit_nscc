import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import FastMarkerCluster, HeatMap, MarkerCluster

#Geospatial data manipulation
import pandas as pd
import geopandas as gpd
import numpy as np
#Used for working with geometrical figures 
from shapely.geometry import Point
#Used for geospatial visualization

import matplotlib.pyplot as plt


##read data with pandas
canadian_cities = pd.read_csv(r"canadacities.csv")
#create geometry column with shapely for use in geopandas
geometry_cities = [ Point(xy) for xy in zip(canadian_cities["lng"],canadian_cities["lat"])   ]
#create geodataframe object 
gdf = gpd.GeoDataFrame(canadian_cities,crs="EPSG:4326",geometry=geometry_cities)

#mean for canada
gdf_mean_lat = np.mean(gdf.lat)
gdf_mean_lng = np.mean(gdf.lng)

#nova scotia latitude and longitude
ns_lat = 44.6923
ns_lng = -62.6572
#### Using streamlit ####
#Set a title for the page
st.title("Clustering Canadian Cities", anchor=None)

#folium map
my_map = folium.Map(tiles='OpenStreetMap',location=[ns_lat,ns_lng], zoom_start=7)
HeatMap(gdf[["lat","lng"]].values.tolist(), name='City Density', show=False, radius=10).add_to(my_map)
#add data from geoJson objects
#folium.GeoJson(data = gdf).add_to(my_map)


#fg = folium.FeatureGroup(name="city")
#fg.add_child(folium.features.GeoJson(gdf))
#my_map.add_child(fg)

#create clusters and add them to map

#my_map.add_child(FastMarkerCluster(gdf[["lat","lng"]].values.tolist(),name="Layer Name"))

locations = gdf[["lat","lng"]].values.tolist()
popup_attributes = gdf[["lat","lng","city","province_name","population","density"]].values.tolist()
popups = ["Latitude:{}<br>Longitude:{}<br>City:{}<br>Province:{}<br>Population:{}<br>Density:{}".format(
    lat, lng, city, province_name, population, density) for (lat, lng, city,province_name,population,density) in popup_attributes]

marker_cluster = MarkerCluster(
    locations=locations,
    popups=popups,
    name="1000 clustered icons",
    overlay=True,
    control=True,

)

marker_cluster.add_to(my_map)


# add a layer control to toggle the layers
folium.LayerControl().add_to(my_map)




#Adding a folium map into a render call using Streamlit.
st_data = st_folium(my_map,width=500,height=500, returned_objects = [])


##Adding sliders to the page
values = st.slider(
    'Range One',
    0.0, 1001.0, (25.0, 750.0))
st.write('Values:', values)

values2 = st.slider(
    'Range Two',
    0.0, 1000.0, (250.0, 750.0))
st.write('Values:', values2)


## adding a map with a pandas dataframe with lat long columns
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)



## adding matplotlib
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)


# create a Folium map centered on the first point
map = folium.Map(location=[gdf['lat'].iloc[0], gdf['lng'].iloc[0]], zoom_start=10)

# add markers for each point in the GeoDataFrame
gdf.apply(lambda row: 
        folium.Marker(location=[row['lat'],row['lng']],
popup=f"City name: {row.city} \n lat,lon:({row.lat},{row.lng})",
tooltip=f"City name: {row.city} \n lat,lon:({row.lat},{row.lng})",
icon=folium.Icon(color="green"),
).add_to(map), axis=1)


# display the map
#### Using streamlit ####
#Set a title for the page
st.title("Adding markers to folium map.", anchor=None)

#Adding a folium map into a render call using Streamlit.
st_data = st_folium(map,width=2000,height=1000, returned_objects = [])