import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Erbil Urban Analysis",
    page_icon="🏙️",
    layout="wide"
)

# Title and description
st.title("Erbil Urban Analysis Dashboard")
st.markdown("""
This dashboard visualizes various urban features of Erbil city including land use, 
climate zones, vegetation, road distribution, and urban density.
""")

# Sidebar
st.sidebar.title("Layer Controls")
show_landuse = st.sidebar.checkbox("Land Use", True)
show_climate = st.sidebar.checkbox("Climate Zones", True)
show_vegetation = st.sidebar.checkbox("Vegetation", True)
show_roads = st.sidebar.checkbox("Roads", True)
show_density = st.sidebar.checkbox("Urban Density", True)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    # Initialize map centered on Erbil
    m = folium.Map(location=[36.191111, 44.009167], zoom_start=13)
    
    # Add your exported data layers here
    # (We'll update this once exports are complete)
    
    # Display map
    folium_static(m)

with col2:
    st.subheader("Statistics")
    st.write("Area Statistics will appear here")
    
    # Add filters
    st.subheader("Filters")
    year_range = st.slider(
        "Select Year Range",
        min_value=2015,
        max_value=2024,
        value=(2020, 2024)
    )
    
    # Add information box
    st.info("""
    Data Sources:
    - Land Use: ESA WorldCover
    - Climate: NASA GLDAS
    - Vegetation: Sentinel-2
    - Urban Density: Google Dynamic World
    """)

# Footer
st.markdown("---")
st.markdown("Created with Google Earth Engine and Streamlit")
