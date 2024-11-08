import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import plotly.express as px
from folium.plugins import HeatMap, Draw, LayerControl

# Remove TimeSliderControl since it's not needed
# from folium.plugins import TimeSliderControl

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

# Layer toggles with additional options
show_landuse = st.sidebar.checkbox("Show Land Use", True)
if show_landuse:
    landuse_types = st.sidebar.multiselect(
        "Select Land Use Types",
        ["Residential", "Commercial", "Industrial", "Green Space"],
        ["Residential", "Commercial"]
    )

show_climate = st.sidebar.checkbox("Show Climate Zones", True)
if show_climate:
    temp_range = st.sidebar.slider(
        "Temperature Range (°C)",
        15, 45, (20, 40)
    )

show_vegetation = st.sidebar.checkbox("Show Vegetation", True)
if show_vegetation:
    vegetation_density = st.sidebar.select_slider(
        "Vegetation Density",
        options=["Low", "Medium", "High"],
        value="Medium"
    )

show_roads = st.sidebar.checkbox("Show Roads", True)
if show_roads:
    road_types = st.sidebar.multiselect(
        "Road Types",
        ["Main Roads", "Secondary Roads", "Local Roads"],
        ["Main Roads"]
    )

show_density = st.sidebar.checkbox("Show Urban Density", True)
if show_density:
    density_threshold = st.sidebar.slider(
        "Density Threshold",
        0, 100, 50
    )

# Time period selection
st.sidebar.subheader("Time Period")
time_range = st.sidebar.slider(
    "Select Year Range",
    2015, 2024, (2020, 2024)
)

# Main content
col1, col2 = st.columns([7, 3])

with col1:
    # Initialize map
    m = folium.Map(
        location=[36.191111, 44.009167],
        zoom_start=13,
        tiles="cartodbpositron"
    )
    
    # Add draw control
    draw = Draw(
        draw_options={
            'polyline': True,
            'rectangle': True,
            'circle': True,
            'marker': True,
        },
        edit_options={'edit': True}
    )
    m.add_child(draw)

    # Sample data visualization (replace with your actual data)
    if show_landuse:
        # Land use polygons
        colors = {
            'Residential': 'blue',
            'Commercial': 'red',
            'Industrial': 'purple',
            'Green Space': 'green'
        }
        for use_type in landuse_types:
            folium.Circle(
                [36.191111 + np.random.random()/100, 
                 44.009167 + np.random.random()/100],
                radius=500,
                popup=use_type,
                color=colors[use_type],
                fill=True,
                fillOpacity=0.4
            ).add_to(m)

    if show_climate:
        # Climate zones heatmap
        heat_data = [
            [36.191111 + np.random.random()/100, 
             44.009167 + np.random.random()/100, 
             np.random.random()] 
            for _ in range(100)
        ]
        HeatMap(heat_data).add_to(m)

    if show_vegetation:
        # Vegetation circles
        vegetation_color = {
            'Low': '#ffeda0',
            'Medium': '#7ec977',
            'High': '#005a32'
        }
        folium.Circle(
            [36.191111, 44.009167],
            radius=300,
            popup=f"Vegetation Density: {vegetation_density}",
            color=vegetation_color[vegetation_density],
            fill=True
        ).add_to(m)

    if show_roads:
        # Road networks
        road_styles = {
            'Main Roads': {'color': 'red', 'weight': 3},
            'Secondary Roads': {'color': 'orange', 'weight': 2},
            'Local Roads': {'color': 'blue', 'weight': 1}
        }
        for road_type in road_types:
            folium.PolyLine(
                [[36.191111, 44.007167], [36.191111, 44.011167]],
                **road_styles[road_type],
                popup=road_type
            ).add_to(m)

    if show_density:
        # Urban density heatmap
        density_data = [
            [36.191111 + np.random.random()/100, 
             44.009167 + np.random.random()/100, 
             np.random.random() * density_threshold/100] 
            for _ in range(100)
        ]
        HeatMap(density_data, gradient={'0.4': 'blue', '0.6': 'lime', '0.8': 'red'}).add_to(m)

    # Add layer control
    LayerControl().add_to(m)
    
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
    
    # Add charts
    st.subheader("Land Use Distribution")
    land_use_data = pd.DataFrame({
        'Category': ['Residential', 'Commercial', 'Industrial', 'Green Space'],
        'Percentage': [40, 25, 20, 15]
    })
    fig = px.pie(land_use_data, values='Percentage', names='Category')
    st.plotly_chart(fig, use_container_width=True)
    
    # Temperature trend
    st.subheader("Temperature Trend")
    temp_data = pd.DataFrame({
        'Month': pd.date_range(start='2023', periods=12, freq='M'),
        'Temperature': np.random.normal(30, 5, 12)
    })
    fig = px.line(temp_data, x='Month', y='Temperature')
    st.plotly_chart(fig, use_container_width=True)

# Footer with metadata
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Data Sources:**")
    st.markdown("- ESA WorldCover")
    st.markdown("- NASA GLDAS")
    st.markdown("- Sentinel-2")
with col2:
    st.markdown("**Update Frequency:**")
    st.markdown("- Land Use: Annual")
    st.markdown("- Climate: Monthly")
    st.markdown("- Vegetation: Seasonal")
with col3:
    st.markdown("**Tools Used:**")
    st.markdown("- Google Earth Engine")
    st.markdown("- Streamlit")
    st.markdown("- Python Geospatial Libraries")

# Add download capability
st.sidebar.markdown("---")
if st.sidebar.button("Download Report"):
    st.sidebar.success("Report downloaded! (Demo)")

# Help section
with st.sidebar.expander("How to Use"):
    st.write("""
    1. Use the checkboxes to show/hide layers
    2. Adjust filters for each layer
    3. Draw areas on map for analysis
    4. Click features for detailed information
    5. Use time slider for temporal analysis
    """)
