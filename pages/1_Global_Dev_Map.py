import streamlit as st
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

st.set_page_config(page_title="Global Dev Map", page_icon="🌍",layout="wide")


# Show the app
st.sidebar.title('📊 **About**')
st.sidebar.text('📈 Visual Analytics Lab 10')
# Add dark mode instructions to the about section
st.sidebar.header('🌙 **Dark Mode**')
st.sidebar.markdown("""
Switch to **Dark Mode** for a visually stunning experience!
1. Click the ⋮ button (three dots) in the top-right corner.
2. Select ⚙️ **Settings**.
3. Enable 🌑 **Dark Mode** for a sleek look!
""")
st.sidebar.markdown('---')  # Separator
st.sidebar.header('✉️ **Contact**')
st.sidebar.text('📧 david.perez18@estudiant.upf.edu')
st.sidebar.markdown('---')  # Separator
st.sidebar.title('🔗 **Source Code**')
st.sidebar.text('👉 [GitHub](https://github.com/dperezz02/HR_Consultancy)')

df3 = pd.read_csv('survey_results_public.csv')
df3 = df3.dropna(subset=['ConvertedCompYearly'])
df3 = df3.dropna(subset=['Country'])
df3 = df3[df3['Country'] != 'Nomadic']
# The title
st.title('Software Developers Geo Data Visualization')
# Get unique countries
unique_countries = df3['Country'].unique()
# @st.cache_data()
# # Function to get coordinates for a country using geopy
# def get_coordinates(country):
#     geolocator = Nominatim(user_agent="geo_locator")
#     location = geolocator.geocode(country)
#     if location:
#         return location.latitude, location.longitude
#     else:
#         return None

# # Create a new DataFrame with unique countries
# coordinates_df = pd.DataFrame({'Country': unique_countries})
# coordinates_df = coordinates_df.dropna()
# # Apply the function to get coordinates for each country
# coordinates_df['Coordinates'] = coordinates_df['Country'].apply(get_coordinates)
# # Filter out rows with missing coordinates
# coordinates_df = coordinates_df.dropna(subset=['Coordinates'])
# # Split the 'Coordinates' column into 'Latitude' and 'Longitude'
# coordinates_df[['Latitude', 'Longitude']] = pd.DataFrame(coordinates_df['Coordinates'].tolist(), index=coordinates_df.index)
# coordinates_df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)
# coordinates_df.loc[coordinates_df['Country'] == 'Egypt', ['lat', 'lon']] = [25.276987, 29.232078]
# coordinates_df.loc[coordinates_df['Country'] == 'China', ['lat', 'lon']] = [35.861660, 104.195397]
# coordinates_df.loc[coordinates_df['Country'] == 'Israel', ['lat', 'lon']] = [31.046051, 34.851612]
# coordinates_df.loc[coordinates_df['Country'] == 'Germany', ['lat', 'lon']] = [51.165691, 10.451526]
# coordinates_df.loc[coordinates_df['Country'] == 'Greece', ['lat', 'lon']] = [39.074208, 21.824312]
# coordinates_df.loc[coordinates_df['Country'] == 'Hungary', ['lat', 'lon']] = [47.162494, 19.503304]
# coordinates_df.loc[coordinates_df['Country'] == 'Sweden', ['lat', 'lon']] = [60.128161, 18.643501]
# coordinates_df.loc[coordinates_df['Country'] == 'Bangladesh', ['lat', 'lon']] = [23.6850, 90.3563]
# coordinates_df.loc[coordinates_df['Country'] == 'Mongolia', ['lat', 'lon']] = [46.8625, 103.8467]
# coordinates_df.loc[coordinates_df['Country'] == 'Lebanon', ['lat', 'lon']] = [33.8547, 35.8623]
# coordinates_df.loc[coordinates_df['Country'] == 'Palestine', ['lat', 'lon']] = [31.9522, 35.2332]
# coordinates_df.loc[coordinates_df['Country'] == 'Georgia', ['lat', 'lon']] = [41.7151, 44.8271]
# coordinates_df.loc[coordinates_df['Country'] == 'Bulgaria', ['lat', 'lon']] = [42.7339, 25.4858]
# coordinates_df.loc[coordinates_df['Country'] == 'Oman', ['lat', 'lon']] = [21.4735, 55.9754]
# coordinates_df.loc[coordinates_df['Country'] == 'Jordan', ['lat', 'lon']] = [30.5852, 36.2384]
# coordinates_df.to_csv('coordinates.csv', index=False)
coordinates_df = pd.read_csv('coordinates.csv')
# Count the number of rows for each country in the original DataFrame
country_counts = df3['Country'].value_counts().reset_index()
country_counts.columns = ['Country', 'Count']

# Merge the counts with the coordinates DataFrame
coordinates_df = pd.merge(coordinates_df, country_counts, on='Country', how='left')
# Create a scatter plot using pydeck with variable-sized circles
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=coordinates_df,
    get_position=["lon", "lat"],
    get_radius="Count * 150+2000",  # Adjust the multiplier based on your preference
    get_fill_color=[0, 0, 255, 100],
    get_text="Count",
    pickable=True,
)

# Set the initial view state
view_state = pdk.ViewState(
    longitude=coordinates_df['lon'].mean(),
    latitude=coordinates_df['lat'].mean(),
    zoom=2,
)

# Create a pydeck map with both layers
deck = pdk.Deck(layers=[scatter_layer], initial_view_state=view_state)
st.subheader("Number of Software Developers by Country")
# Display the map in Streamlit
st.pydeck_chart(deck, use_container_width=True)

country_salary_mean = df3.groupby('Country')['ConvertedCompYearly'].mean().reset_index()
country_salary_mean.columns = ['Country', 'MeanSalary']
# Merge the counts with the coordinates DataFrame
coordinates_df = pd.merge(coordinates_df, country_salary_mean, on='Country', how='left')

hexagon_layer = pdk.Layer(
    "HexagonLayer",
    data=coordinates_df,
    get_position=["lon", "lat"],
    getElevationWeight="MeanSalary",
    getColorWeight="Count",
    auto_highlight=True,
    elevation_scale=1000,  # Adjust the elevation scale based on your preference
    elevation_range=[0, 20000],  # Adjust the range of elevation
    extruded=True,
    coverage=1,
    radius=100000,  # Adjust the radius of hexagons based on your preference
)

# Set the initial view state
view_state = pdk.ViewState(
    longitude=coordinates_df['lon'].mean(),
    latitude=coordinates_df['lat'].mean(),
    zoom=2,
    pitch=90
)

# Create a pydeck map with the hexagon layer
deck = pdk.Deck(layers=[hexagon_layer], initial_view_state=view_state)

# Display the map in Streamlit
st.subheader("Mean Salary by Country")
st.write("Color defines the number of developers from each country.")
st.write( ":large_red_square: -> More developers")
st.write(":large_yellow_circle: -> Less developers")
st.pydeck_chart(deck, use_container_width=True)


# Display an interactive table with country, mean salary, and number of developers
sorted_coordinates_df = coordinates_df.sort_values(by='Count', ascending=False)
st.subheader("Table of Software Developers and Mean Salary by Country")
# Format Mean Salary to remove decimals
sorted_coordinates_df['MeanSalary'] = sorted_coordinates_df['MeanSalary'].astype(int)
sorted_coordinates_df.rename(columns={'MeanSalary': 'Mean Salary ($)'}, inplace=True)
sorted_coordinates_df.rename(columns={'Count': 'Number of Software Developers'}, inplace=True)
st.dataframe(sorted_coordinates_df[['Country', 'Number of Software Developers', 'Mean Salary ($)']], use_container_width=True)