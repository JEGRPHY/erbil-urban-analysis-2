import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import plotly.express as px
import ee
import geemap.foliumap as geemap

# Initialize Earth Engine
try:
    # Trigger the authentication flow.
    ee.Initialize(project='erbil-analysis')
    st.success("Successfully connected to Google Earth Engine!")
except:
    st.error("Failed to connect to Google Earth Engine. Please check your authentication.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Erbil Urban Analysis",
    page_icon="🏙️",
    layout="wide"
)

# Title and description
st.title("Erbil Urban Analysis Dashboard")
st.markdown("""
This interactive dashboard visualizes various urban features of Erbil city using real-time data from Google Earth Engine.
""")

# Define Erbil area
ERBIL_CENTER = ee.Geometry.Point([44.009167, 36.191111])
ERBIL_AREA = ERBIL_CENTER.buffer(5000)  # 5km radius

# Sidebar controls
st.sidebar.title("Map Controls")

# Date selection
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-01-01"))

# Layer controls
show_landuse = st.sidebar.checkbox("Show Land Use", True)
show_ndvi = st.sidebar.checkbox("Show Vegetation (NDVI)", False)
show_temperature = st.sidebar.checkbox("Show Temperature", False)
show_urban = st.sidebar.checkbox("Show Urban Areas", False)

# Main content
col1, col2 = st.columns([7, 3])

with col1:
    # Create an Earth Engine-enabled folium map
    Map = geemap.Map(center=[36.191111, 44.009167], zoom=12)
    
    if show_landuse:
        # Get land use data from ESA WorldCover
        landcover = ee.ImageCollection("ESA/WorldCover/v200").first()
        vis_params = {
            'bands': ['Map'],
        }
        Map.addLayer(landcover.clip(ERBIL_AREA), vis_params, 'Land Use')

    if show_ndvi:
        # Calculate NDVI from Sentinel-2
        s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(ERBIL_AREA) \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median()
        
        ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndvi_vis = {'min': -1, 'max': 1, 'palette': ['red', 'white', 'green']}
        Map.addLayer(ndvi.clip(ERBIL_AREA), ndvi_vis, 'NDVI')

    if show_temperature:
        # Get temperature data
        temperature = ee.ImageCollection('NASA/GLDAS/V021/NOAH/G025/T3H') \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .select('SoilTMP0_10cm_inst') \
            .mean()
        
        temp_vis = {'min': 270, 'max': 310, 'palette': ['blue', 'yellow', 'red']}
        Map.addLayer(temperature.clip(ERBIL_AREA), temp_vis, 'Temperature')

    if show_urban:
        # Get urban areas from Dynamic World
        urban = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1') \
            .filterBounds(ERBIL_AREA) \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .select('built') \
            .mean()
        
        urban_vis = {'min': 0, 'max': 1, 'palette': ['white', 'red']}
        Map.addLayer(urban.clip(ERBIL_AREA), urban_vis, 'Urban Areas')

    # Add the drawing tools
    Map.add_draw_control()
    # Add layer control
    Map.add_layer_control()

    # Display the map
    Map.to_streamlit(height=600)

with col2:
    st.subheader("Area Analysis")
    
    if show_ndvi:
        # Calculate NDVI statistics
        ndvi_stats = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=ERBIL_AREA,
            scale=30
        ).getInfo()
        
        st.metric("Average NDVI", f"{ndvi_stats['NDVI']:.2f}")

    if show_urban:
        # Calculate urban area statistics
        urban_stats = urban.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=ERBIL_AREA,
            scale=30
        ).getInfo()
        
        st.metric("Urban Density", f"{urban_stats['built']*100:.1f}%")

    # Add charts based on GEE data
    if show_temperature:
        # Get temperature time series
        temp_chart = ee.ImageCollection('NASA/GLDAS/V021/NOAH/G025/T3H') \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .select('SoilTMP0_10cm_inst') \
            .getRegion(ERBIL_AREA, 30)
        
        # Convert to pandas dataframe
        temp_data = pd.DataFrame(temp_chart.getInfo())
        if len(temp_data) > 0:
            temp_data.columns = ['id', 'longitude', 'latitude', 'time', 'temperature']
            temp_data['time'] = pd.to_datetime(temp_data['time'], unit='ms')
            
            fig = px.line(temp_data, x='time', y='temperature', 
                         title='Temperature Trend')
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
Data Sources:
- Land Use: ESA WorldCover
- Vegetation: Sentinel-2
- Temperature: NASA GLDAS
- Urban Areas: Dynamic World
""")
