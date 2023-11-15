import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import pickle
import matplotlib.pyplot as plt
import altair as alt
import matplotlib.pyplot as plt


st.set_page_config(page_title="Complex Salary Prediction", page_icon="💲",layout="wide")
st.title('Complex Salary Prediction')


# Show the app
st.sidebar.title('📊 **About**')
st.sidebar.text('📈 Visual Analytics Lab 10')
# Add dark mode instructions to the about section
# Display a disclaimer about the accuracy of the model
st.sidebar.info(
    "⚠️ **Disclaimer:**\n"
    "This salary prediction model is a beta version and has limited accuracy. It considers the exact job position "
    "and the type of organization but may not provide reliable predictions. For realistic predictions, please use the "
    "Salary Prediction page. The Complex Prediction page is designed to give an idea of relative differences between "
    "salaries for different job positions, but the values are not accurate. Use the predictions taking this into consideration."
)
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

with open('saved_steps2.pkl', 'rb') as file:
    data = pickle.load(file)

df = pd.read_csv('complex.csv')

regressor_loaded = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_devtype = data["le_devtype"]

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
sorted_org_values = sorted(df['OrgSize'].unique(), key=lambda x: float(x))
# Use the sorted values in the selectbox
selected_org_size = st.slider(
    'Select Size of Organization',
    min_value=int(min(sorted_org_values)),
    max_value=int(max(sorted_org_values)),
    step=1,  # Set step to 1 to allow only integer values
    key='org_size_selector'
)
selected_education = st.selectbox('Select an Education Level', df['EdLevel'].unique(), key='education_selector', index=1)
selected_type = st.selectbox('Select an Developer Type', df['DevType'].unique(), key='developer_type_selector', index=1)
# Transform the selected inputs using the label encoders
encoded_country = le_country.transform([selected_country])
encoded_education = le_education.transform([selected_education])
encoded_type = le_devtype.transform([selected_type])

input_data = pd.DataFrame({
    'Country': encoded_country,
    'EdLevel': encoded_education,
    'YearsCodePro': selected_experience,
    'OrgSize': selected_org_size,
    'DevType': encoded_type
})
# Use the model to predict the salary
predicted_salary = regressor_loaded.predict(input_data)

# Display the predicted salary
st.markdown(f'## The predicted salary is: **{np.round(predicted_salary[0],2)}$**')
