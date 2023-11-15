import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import time
import pickle
import matplotlib.pyplot as plt
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Human Resources Consultancy",
    page_icon="📊",
)

# Load the data
df = pd.read_csv('countries.csv')
df2 = pd.read_csv('encoded.csv')

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

# The title
st.title('Exploratory Data Analysis')

# Data Table
st.subheader('Interactive Data Table')
st.dataframe(df, use_container_width=True)

# Summary statistics
st.subheader('Summary Statistics')
st.write(df.describe())

# Visualize the number of null values in each variable
st.write('Number of Nulls in Each Variable')
null_counts = df.isnull().sum()
# Display as a table with a label for the total
null_counts_with_total = pd.DataFrame(null_counts).T
null_counts_with_total.index = ['Total Nulls']
st.table(null_counts_with_total)

# Correlation Heatmap
correlation_matrix = df2.corr()
# Convert the correlation matrix to a long format
correlation_long = correlation_matrix.unstack().reset_index(name='correlation')
correlation_long = correlation_long.rename(columns={'level_0': 'Variable 1', 'level_1': 'Variable 2'})
# Create an Altair Chart
chart = alt.Chart(correlation_long).mark_rect().encode(
    x='Variable 1:N',
    y='Variable 2:N',
    color=alt.Color('correlation:Q', scale=alt.Scale(scheme='reds'))
).properties(
    width=600,
    height=600,
    title={"text": "Correlation Heatmap", "anchor": "middle", "fontSize": 16, "color": "white"}
)
# Display the Altair Chart
st.altair_chart(chart, use_container_width=True)

# Bar Chart
st.subheader("Salary Distribution per Country")
bar_chart_data = df.groupby('Country')['Salary'].median().sort_values(ascending=False).reset_index()
bar_chart = alt.Chart(bar_chart_data).mark_bar().encode(
    x=alt.X('Country:N', title='Country'),
    y=alt.Y('Salary:Q', title='Median Salary ($)'),
)
st.altair_chart(bar_chart,use_container_width=True)

# Area Chart
st.subheader("Salary Distribution per Experience")
area_chart_data = df.groupby('YearsCodePro')['Salary'].median().sort_values(ascending=False).reset_index()
area_chart = alt.Chart(area_chart_data).mark_area().encode(
    x=alt.X('YearsCodePro:N', title='Years of Experience'),
    y=alt.Y('Salary:Q', title='Median Salary ($)'),
)
st.altair_chart(area_chart,use_container_width=True)

# Bar Chart
st.subheader("Salary Distribution per Education Level")
bar_chart_data = df.groupby('EdLevel')['Salary'].median().sort_values(ascending=False).reset_index()
bar_chart = alt.Chart(bar_chart_data).mark_bar().encode(
    x=alt.X('EdLevel:N', title='Education Level'),
    y=alt.Y('Salary:Q', title='Median Salary ($)'),
)
st.altair_chart(bar_chart,use_container_width=True)

# Set Seaborn to use Streamlit dark theme
sns.set_theme(style="darkgrid")

@st.cache_data() #This function takes more time than the rest of them, so I store it in cache for faster reloading
def boxplot():
    # Box Plot
    st.subheader("Box Plot Distribution per Country")
    fig, ax = plt.subplots(figsize=(14, 10))

    # Define a custom color palette for better visibility
    custom_palette = sns.color_palette("bright", n_colors=50)

    # Sort the dataframe by median salary per country
    sorted_countries = df.groupby('Country')['Salary'].median().sort_values(ascending=False).index

    # Set the background to black
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'

    # Plotting the boxplot for filtered salaries per country with customizations
    box_plot = sns.boxplot(x='Country', y='Salary', data=df, palette=custom_palette, order=sorted_countries, showfliers=True, ax=ax)

    for flier in box_plot.lines:
        flier.set_markeredgecolor('white')
        flier.set_markerfacecolor('white')

    # Change the color of the outlier points and the lines of the boxplots
    for i, artist in enumerate(box_plot.artists):
        col = artist.get_facecolor()

        # Change the color of the lines of the boxplots to match the box color
        for j in range(6*i, 6*(i+1)):
            box_plot.lines[j].set_color(col)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, color='white', fontsize=15)  # Set the axis label color and font size
    ax.tick_params(axis='both', colors='white', labelsize=15)
    ax.set_xlabel('Country', color='white', fontsize=22)  # Set the axis label color and font size
    ax.set_ylabel('Salary ($)', color='white', fontsize=22)  # Set the axis label color and font size
    ax.set_title('Box Plot of Salary per Country', color='white', fontsize=30)  # Set the title color and font size
    ax.set_facecolor('black')  # Set the plot background color to black

    # Set the background color of the entire figure to black
    fig.patch.set_facecolor('#0E1117')

    # Customize the grid lines for better visibility
    ax.grid(axis='y', linestyle='--', alpha=0.7, color='white')

    # Highlight the median line inside the boxplot
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .3))
        patch.set_edgecolor((r, g, b, 1))

    # Annotate the country with the highest median salary
    highest_country = df.groupby('Country')['Salary'].median().sort_values(ascending=False).index[0]

    st.pyplot(fig, clear_figure=True)
boxplot()

# Violin plot per selected country
st.subheader(f"Violin Plot by selected Country")
# User selects a country
selected_country = st.selectbox('Select a Country', df['Country'].unique(), index=3)
# Filter data for the selected country
selected_data = df[df['Country'] == selected_country]
# Plot the salary distribution for the selected country using Violin Plot
fig, ax = plt.subplots(figsize=(15, 10))
color = 'skyblue'  # Set the desired color for the entire violin plot
sns.violinplot(x='Country', y='Salary', data=selected_data, ax=ax, color=color)
ax.set_xlabel('Country', color='white', fontsize=20)  # Set the axis label color and font size
ax.set_ylabel('Salary ($)', color='white', fontsize=20)  # Set the axis label color and font size
ax.set_title(f'Salary Distribution for {selected_country}', color='white', fontsize=24)  # Set the title color and font size
ax.set_facecolor('black')  # Set the plot background color to black
ax.tick_params(axis='both', colors='white', labelsize=15)
# Set the background color of the entire figure to black
fig.patch.set_facecolor('#0E1117')
# Customize the grid lines for better visibility
ax.grid(axis='y', linestyle='--', alpha=0.7, color='white')
# Display the plot in Streamlit
st.pyplot(fig)

# Violin plot per education level
st.subheader("Violin Plot by selected Education Level")
# User selects an education level
selected_education = st.selectbox('Select an Education Level', df['EdLevel'].unique(), index=2)
# Filter data for the selected education level
selected_education_data = df[df['EdLevel'] == selected_education]
# Plot the salary distribution for the selected education level using Violin Plot
fig_edu, ax_edu = plt.subplots(figsize=(15, 10))
color_edu = 'lightcoral'  # Set the desired color for the entire violin plot
sns.violinplot(x='EdLevel', y='Salary', data=selected_education_data, ax=ax_edu, color=color_edu)
ax_edu.set_xlabel('Education Level', color='white', fontsize=20)  # Set the axis label color and font size
ax_edu.set_ylabel('Salary ($)', color='white', fontsize=20)  # Set the axis label color and font size
ax_edu.set_title(f'Salary Distribution for {selected_education}', color='white', fontsize=24)  # Set the title color and font size
ax_edu.set_facecolor('black')  # Set the plot background color to black
ax_edu.tick_params(axis='both', colors='white', labelsize=15)
# Set the background color of the entire figure to black
fig_edu.patch.set_facecolor('#0E1117')
# Customize the grid lines for better visibility
ax_edu.grid(axis='y', linestyle='--', alpha=0.7, color='white')
# Display the plot in Streamlit
st.pyplot(fig_edu)

# Violin plot with multiple selection options
st.subheader("Violin Plot by Country, Years of Experience, and Education Level")
# User selects a country
selected_country = st.selectbox('Select a Country', df['Country'].unique(), key='country_selector', index=16)
# User selects years of experience
sorted_experience_values = sorted(df['YearsCodePro'].unique(), key=lambda x: float(x))
# Use the sorted values in the selectbox
selected_experience = st.selectbox('Select Years of Experience', sorted_experience_values, key='experience_selector')# User selects education level
selected_education = st.selectbox('Select an Education Level', df['EdLevel'].unique(), key='education_selector', index=1)
# Filter data based on user selections
selected_data = df[(df['Country'] == selected_country) & 
                   (df['YearsCodePro'] == selected_experience) & 
                   (df['EdLevel'] == selected_education)]

# Check if the selected combination has data
if selected_data.empty:
    # Display a message indicating no data for the selected combination
    st.subheader("No Data Available 😕")
    st.markdown("Sorry, there is no data for the selected combination. Please try another combination. 🔄")
else:
    # Plot the salary distribution for the selected options using Violin Plot
    fig, ax = plt.subplots(figsize=(15, 10))
    color = 'orange'  # Set the desired color for the entire violin plot
    sns.violinplot(x='Country', y='Salary', data=selected_data, ax=ax, color=color)
    ax.set_xlabel('Country', color='white', fontsize=20)  # Set the axis label color and font size
    ax.set_ylabel('Salary ($)', color='white', fontsize=20)  # Set the axis label color and font size
    ax.set_title(f'Salary Distribution for {selected_country}, {selected_experience} Years of Experience, and {selected_education}', color='white', fontsize=24)  # Set the title color and font size
    ax.set_facecolor('black')  # Set the plot background color to black
    ax.tick_params(axis='both', colors='white', labelsize=15)
    # Set the background color of the entire figure to black
    fig.patch.set_facecolor('#0E1117')
    # Customize the grid lines for better visibility
    ax.grid(axis='y', linestyle='--', alpha=0.7, color='white')
    # Display the plot in Streamlit
    st.pyplot(fig)


# Data Download
st.subheader('Download Processed Data')
if st.button('Download Data as CSV'):
    df.to_csv('processed_data.csv', index=False)
    st.success('Data downloaded successfully!')