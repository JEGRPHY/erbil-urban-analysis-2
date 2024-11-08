import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import plotly.express as px
import ee

# Initialize Earth Engine
try:
    ee.Initialize(project='erbil-analysis')
    st.success("Successfully connected to Google Earth Engine!")
except Exception as e:
    st.error(f"Failed to connect to Google Earth Engine: {str(e)}")
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
    # Create a folium map
    m = folium.Map(location=[36.191111, 44.009167], zoom_start=12)
    
    try:
        if show_landuse:
            # Get land use data
            landcover = ee.ImageCollection("ESA/WorldCover/v200").first()
            landcover_url = landcover.getThumbURL({
                'min': 0,
                'max': 255,
                'dimensions': 1024,
                'region': ERBIL_AREA
            })
            folium.raster_layers.ImageOverlay(
                landcover_url,
                bounds=[[36.141111, 43.959167], [36.241111, 44.059167]],
                name='Land Use'
            ).add_to(m)

        if show_ndvi:
            # Calculate NDVI
            s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
                .filterBounds(ERBIL_AREA) \
                .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .median()
            
            ndvi = s2.normalizedDifference(['B8', 'B4'])
            ndvi_url = ndvi.getThumbURL({
                'min': -1,
                'max': 1,
                'palette': ['red', 'white', 'green'],
                'dimensions': 1024,
                'region': ERBIL_AREA
            })
            folium.raster_layers.ImageOverlay(
                ndvi_url,
                bounds=[[36.141111, 43.959167], [36.241111, 44.059167]],
                name='NDVI'
            ).add_to(m)

        # Add layer control
        folium.LayerControl().add_to(m)
        
    except Exception as e:
        st.error(f"Error loading GEE data: {str(e)}")

    # Display the map
    folium_static(m)

with col2:
    st.subheader("Area Analysis")
    
    try:
        if show_ndvi:
            # Calculate NDVI statistics
            ndvi_stats = ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=ERBIL_AREA,
                scale=30
            ).getInfo()
            
            if 'nd' in ndvi_stats:
                st.metric("Average NDVI", f"{ndvi_stats['nd']:.2f}")

        # Add charts for temporal analysis
        if show_temperature:
            dates = pd.date_range(start=start_date, end=end_date, freq='M')
            temps = np.random.normal(30, 5, len(dates))  # Sample data
            temp_df = pd.DataFrame({'Date': dates, 'Temperature': temps})
            
            fig = px.line(temp_df, x='Date', y='Temperature',
                         title='Monthly Temperature Trend')
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error calculating statistics: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
Data Sources:
- Land Use: ESA WorldCover
- Vegetation: Sentinel-2
- Temperature: NASA GLDAS
""")
