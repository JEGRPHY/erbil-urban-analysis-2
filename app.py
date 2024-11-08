import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
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
This interactive dashboard visualizes various urban features of Erbil city, including:
- Land Use Distribution
- Local Climate Zones
- Vegetation Coverage
- Road Network
- Urban Density Patterns
""")

# Sidebar controls
st.sidebar.title("Map Controls")

# Layer toggles
show_landuse = st.sidebar.checkbox("Show Land Use", True)
show_climate = st.sidebar.checkbox("Show Climate Zones", True)
show_vegetation = st.sidebar.checkbox("Show Vegetation", True)
show_roads = st.sidebar.checkbox("Show Roads", True)
show_density = st.sidebar.checkbox("Show Urban Density", True)

# Main content
col1, col2 = st.columns([7, 3])

with col1:
    # Initialize map
    m = folium.Map(
        location=[36.191111, 44.009167],
        zoom_start=13,
        tiles="cartodbpositron"
    )
    
    # Basic feature demonstration
    if show_landuse:
        folium.Circle(
            [36.191111, 44.009167],
            radius=500,
            popup="Commercial Area",
            color='red',
            fill=True,
            fillOpacity=0.4
        ).add_to(m)

    if show_roads:
        folium.PolyLine(
            [[36.191111, 44.007167], [36.191111, 44.011167]],
            color="blue",
            weight=3,
            popup="Main Road"
        ).add_to(m)
    
    # Display map
    folium_static(m)

with col2:
    # Statistics and Analysis
    st.subheader("Area Statistics")
    
    # Sample metrics
    metrics = {
        "Total Area": "25 km²",
        "Population": "850,000",
        "Green Space": "15%",
        "Road Network": "320 km",
        "Built-up Area": "60%"
    }
    
    for metric, value in metrics.items():
        st.metric(metric, value)
    
    # Add simple chart
    st.subheader("Land Use Distribution")
    land_use_data = pd.DataFrame({
        'Category': ['Residential', 'Commercial', 'Industrial', 'Green Space'],
        'Percentage': [40, 25, 20, 15]
    })
    fig = px.pie(land_use_data, values='Percentage', names='Category')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Data sources: OpenStreetMap, Earth Engine, Sentinel-2")
