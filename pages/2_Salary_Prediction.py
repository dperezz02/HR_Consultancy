import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import pickle
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title="Salary Prediction", page_icon="💴",layout="wide")
st.title('Salary Prediction')


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

with open('saved_steps.pkl', 'rb') as file:
    data = pickle.load(file)

df = pd.read_csv('countries.csv')

regressor_loaded = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

# User selects a country
selected_country = st.selectbox('Select a Country', df['Country'].unique(), key='country_selector', index=16)
# User selects years of experience
sorted_experience_values = sorted(df['YearsCodePro'].unique(), key=lambda x: float(x))
# Use the sorted values in the selectbox
selected_experience = max(0.5,st.slider(
    'Select Years of Experience',
    min_value=int(min(sorted_experience_values)),
    max_value=int(max(sorted_experience_values)),
    step=1,  # Set step to 1 to allow only integer values
    key='experience_selector'
))
selected_education = st.selectbox('Select an Education Level', df['EdLevel'].unique(), key='education_selector', index=1)
# Transform the selected inputs using the label encoders
encoded_country = le_country.transform([selected_country])
encoded_education = le_education.transform([selected_education])

input_data = pd.DataFrame({
    'Country': encoded_country,
    'EdLevel': encoded_education,
    'YearsCodePro': selected_experience
})
# Use the model to predict the salary
predicted_salary = regressor_loaded.predict(input_data)

# Display the predicted salary
st.markdown(f'## The predicted salary is: **{np.round(predicted_salary[0],2)}$**')

# Calculate mean salary for selected country, education level, and years of experience
mean_salary_country = df[df['Country'] == selected_country]['Salary'].mean()
mean_salary_education = df[df['EdLevel'] == selected_education]['Salary'].mean()
mean_salary_experience = df[df['YearsCodePro'] == selected_experience]['Salary'].mean()
# Create a bar chart using Streamlit
st.subheader('Salary Comparison')
# Create a DataFrame for visualization
comparison_data = pd.DataFrame({
    'Category': ['Predicted Salary', f'{selected_country} Average Salary', f'{selected_education} Average Salary', f'Average Salary for {selected_experience} years of experience'],
    'Salary': [int(predicted_salary[0]), int(mean_salary_country), int(mean_salary_education), int(mean_salary_experience)]
})

# Set colors for each bar
colors = ['blue', 'green', 'orange', 'red']

# Create an Altair bar chart
chart = alt.Chart(comparison_data).mark_bar().encode(
    x=alt.X('Category:N', title=None, axis=alt.Axis(labelAngle=0)),  # Rotate x-axis labels
    y='Salary',
    color=alt.Color('Category', scale=alt.Scale(range=colors)),
    tooltip=['Category', 'Salary']
).properties(
    width=alt.Step(80)  # Adjust the width based on your preference
)

# Add white labels inside the bars
text = chart.mark_text(
    align='center',
    baseline='middle',
    dy=20,  # Adjust vertical position of the label
    fill='white',  # Set background color to black
    fontSize=14,
).encode(
    text='Salary:Q'
)

# Display the Altair chart with labels inside the bars in Streamlit
st.altair_chart(chart + text, use_container_width=True)

# Calculate the percentage differences
percentage_difference_country = ((predicted_salary - mean_salary_country) / mean_salary_country) * 100
percentage_difference_education = ((predicted_salary - mean_salary_education) / mean_salary_education) * 100
percentage_difference_experience = ((predicted_salary - mean_salary_experience) / mean_salary_experience) * 100

# Extract scalar values
percentage_difference_country2 = np.abs(percentage_difference_country)[0]
percentage_difference_education2 = np.abs(percentage_difference_education)[0]
percentage_difference_experience2 = np.abs(percentage_difference_experience)[0]

# Display visual text with emojis
st.subheader("Comparison with Mean Salaries")
st.markdown(f"Your predicted salary is **{percentage_difference_country2:.0f}%** <span style='color: {'green' if percentage_difference_country > 0 else 'red'};'>{'higher' if percentage_difference_country > 0 else 'lower'}</span> than {selected_country}'s mean software developers' salary! 🌍💻", unsafe_allow_html=True)
st.markdown(f"Your predicted salary is **{percentage_difference_education2:.0f}%** <span style='color: {'green' if percentage_difference_education > 0 else 'red'};'>{'higher' if percentage_difference_education > 0 else 'lower'}</span> than software developers with {selected_education} mean salary! 🎓💵", unsafe_allow_html=True)
st.markdown(f"Your predicted salary is **{percentage_difference_experience2:.0f}%** <span style='color: {'green' if percentage_difference_experience > 0 else 'red'};'>{'higher' if percentage_difference_experience > 0 else 'lower'}</span> than software developers with {selected_experience} years of experience mean salary! ⌛💼", unsafe_allow_html=True)

st.subheader("Salary Predictions by Years of Experience")
# User selects a country for line chart
selected_country_linechart = st.selectbox('Select a Country for Line Chart', df['Country'].unique(), key='country_linechart_selector', index=16)

# User selects education level for line chart
selected_education_linechart = st.selectbox('Select an Education Level for Line Chart', df['EdLevel'].unique(), key='education_linechart_selector', index=1)

# Transform the selected inputs using the label encoders
encoded_country_linechart = le_country.transform([selected_country_linechart])
encoded_education_linechart = le_education.transform([selected_education_linechart])

# Generate a range of years of experience
years_of_experience_range = range(0, 51)

# Predict salary for each year of experience
predicted_salaries_linechart = []
for experience in years_of_experience_range:
    input_data_linechart = pd.DataFrame({
        'Country': encoded_country_linechart,
        'EdLevel': encoded_education_linechart,
        'YearsCodePro': experience
    })

    # Use the model to predict the salary
    predicted_salary_linechart = regressor_loaded.predict(input_data_linechart)
    predicted_salaries_linechart.append(predicted_salary_linechart[0])

# Line chart
linechart_data = pd.DataFrame({
    'Years of Experience': years_of_experience_range,
    'Predicted Salary': predicted_salaries_linechart
})
# Altair Line Chart
line_chart = alt.Chart(linechart_data).mark_line().encode(
    x=alt.X('Years of Experience:O', title='Years of Experience'),
    y=alt.Y('Predicted Salary:Q', title='Predicted Salary ($)'),
)
st.subheader(f'Predicted Salary Trend in {selected_country_linechart} with {selected_education_linechart} by Years of Experience')
# Display the Altair line chart
st.altair_chart(line_chart, use_container_width=True)

# User selects a country for the multi-line chart
selected_country_multiline = st.selectbox('Select a Country for Multi-Line Chart', df['Country'].unique(), key='country_multiline_selector', index=16)
encoded_country_multiline = le_country.transform([selected_country_multiline])
# Generate a range of years of experience
years_of_experience_range = range(0, 51)

# Initialize a list to store data for each education level
multiline_data = []

# Predict salary for each year of experience and each education level
for education_level in df['EdLevel'].unique():
    encoded_education_multiline = le_education.transform([education_level])
    
    predicted_salaries_multiline = []
    for experience in years_of_experience_range:
        input_data_multiline = pd.DataFrame({
            'Country': encoded_country_multiline,
            'EdLevel': encoded_education_multiline,
            'YearsCodePro': experience
        })

        # Use the model to predict the salary
        predicted_salary_multiline = regressor_loaded.predict(input_data_multiline)
        predicted_salaries_multiline.append(predicted_salary_multiline[0])

    # Add data for the current education level to the list
    multiline_data.append({
        'Years of Experience': list(years_of_experience_range),
        'Predicted Salary': predicted_salaries_multiline,
        'Education Level': [education_level] * len(years_of_experience_range)
    })

# Combine data for all education levels into a single DataFrame
multiline_data = pd.concat([pd.DataFrame(data) for data in multiline_data])

# Altair Multi-Line Chart
multiline_chart = alt.Chart(multiline_data).mark_line().encode(
    x=alt.X('Years of Experience:O', title='Years of Experience'),
    y=alt.Y('Predicted Salary:Q', title='Predicted Salary ($)'),
    color='Education Level:N'
)
st.subheader(f'Predicted Salary Trend for {selected_country_multiline} by Education Level and Years of Experience')
# Display the Altair multi-line chart
st.altair_chart(multiline_chart, use_container_width=True)