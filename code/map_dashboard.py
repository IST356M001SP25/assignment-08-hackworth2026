'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

df = pd.read_csv('./cache/top_locations_mappable.csv')

# Page header
st.title('Syracuse Parking Ticket Hotspots')
st.caption('View the Syracuse locations with over $1,000 in parking violation totals.')

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))

# Initialize folium map
m = folium.Map(location=CUSE, zoom_start=ZOOM)

# Add data layer to map
cuse_map = gdf.explore(
    column='amount',
    cmap='magma',
    vmin=VMIN,
    vmax=VMAX,
    legend=True,
    legend_kwds={'caption': 'Amount'},
    marker_type='circle',
    marker_kwds={'radius': 10, 'fill': True},
    m=m
)

# Display map in Streamlit
sf.folium_static(cuse_map, width=800, height=600)