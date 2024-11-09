import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import pickle

# Load the trained model
with open('zepto_time_estimator.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the data
eta_cc_df = pd.read_csv('zepto_cdf.csv')
eta_encoded_df = pd.read_csv('zepto_edf.csv')

# Title and Description
st.markdown(
    """
    <h1 style='text-align: center;'>
        <span style='color:#F72585;'>Zepto</span> <span style='color:#7209B7;'>Delivery Time Estimator</span>
    </h1>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Made By : <b><a href='https://www.linkedin.com/in/prasadmjadhav2/'>Prasad M. Jadhav</a></b>",
    unsafe_allow_html=True
)

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;"/>""",unsafe_allow_html=True)

# Define the categorical columns
categorical_columns = ['delivery_slot', 'weather_conditions', 'traffic_conditions',
       'payment_method', 'product_category', 'order_fulfillment_status',
       'customer_location', 'delivery_type']

# Define the numerical columns (integers and floats separately)
numerical_columns_int = ['store_id', 'num_items', 'packaging_time_seconds']
numerical_columns_float = ['delivery_distance_km', 'order_value', 'delivery_person_experience_years']

# Create a dictionary to map original values to encoded values
encoded_dict = {col: dict(zip(eta_cc_df[col], eta_encoded_df[col])) for col in categorical_columns}

# Selection for categorical columns
selected_encoded_values = {}
for col in categorical_columns:
    unique_values = eta_cc_df[col].unique()
    
    # Create a selectbox for each categorical column
    selected_value = st.selectbox(f'Select {col}', unique_values)
    encoded_value = encoded_dict[col][selected_value]
    selected_encoded_values[col] = encoded_value

# Input fields for numerical columns (integer)
numerical_values = {}
for col in numerical_columns_int:
    value = st.number_input(f'Enter {col}', min_value=0, step=1)  # step=1 ensures integer input
    numerical_values[col] = value

# Input fields for numerical columns (float)
for col in numerical_columns_float:
    value = st.number_input(f'Enter {col}', min_value=0.0)
    numerical_values[col] = value

# Combine categorical and numerical inputs
input_data = np.array([list(selected_encoded_values.values()) + list(numerical_values.values())])

# Prediction
if st.button('Predict'):
    prediction = model.predict(input_data)[0]
    minutes = int(prediction)  # Get the integer part for minutes
    seconds = int((prediction - minutes) * 60)  # Calculate seconds from the decimal part
    st.write(f'Your Delivery Order Time Estimate: {minutes}.{seconds}')
