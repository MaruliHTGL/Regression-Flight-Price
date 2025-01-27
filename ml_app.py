# import ml package
import joblib
import os

import streamlit as st
import numpy as np
import pandas as pd
import datetime

from scipy.stats import skew
from scipy.special import boxcox1p
        
def load_scaler(scaler_file):
    loaded_scaler = joblib.load(open(os.path.join(scaler_file), 'rb'))
    return loaded_scaler
        
def load_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file), 'rb'))
    return loaded_model

def run_ml_app():
    st.markdown("<h2 style = 'text-align: center;'> Input Your Flight Data </h2>", unsafe_allow_html=True)

    airline = st.selectbox("Airline", ['LCC', 'Full service', 'Full service premium economy', 'Full service business', 
                                       'Multiple carriers', 'Multiple carriers premium economy'])
    date = st.date_input("Date of Journey", datetime.date(2019, 7, 6))
    hour = st.slider("Flight Hours Duration", 0, 24, 5)
    minute = st.slider("Flight Minutes Duration", 0, 60, 30)
    info = st.selectbox("Additional Info", ['No info', 'No check-in baggage included', 'In-flight meal not included', 
                                            'Business class', 'Change airports', 'Red-eye flight',
                                            '1 Short layover', '1 Long layover', '2 Long layover'
                                            ])

    st.markdown("<h2 style = 'text-align: center;'>Your Flight Data </h2>", unsafe_allow_html=True)

    df = pd.DataFrame(
        {
            'Airline': [airline],
            'Date': [date],
            'Hours': [hour],
            'Minutes': [minute],
            'Additional Info': [info]
        }
    )

    st.dataframe(df)

    st.markdown("<h2 style = 'text-align: center;'> Prediction Result </h2>", unsafe_allow_html=True)

    duration = hour * 60 + minute

    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

    day = df['Date'].dt.day.values[0]
    month = df['Date'].dt.month.values[0]

    result = {
            'day': int(day),
            'month': int(month),
            'duration': float(boxcox1p(duration, 0.20)),
            'airline': airline,
            'info': info
    }

    # Map geography to one-hot encoding
    airline_dict = {'Full service'                     : [1, 0, 0, 0, 0, 0], 
                    'Full service business'            : [0, 1, 0, 0, 0, 0], 
                    'LCC'                              : [0, 0, 0, 1, 0, 0],
                    'Multiple carriers'                : [0, 0, 0, 0, 1, 0],
                    'Multiple carriers premium economy': [0, 0, 0, 0, 0, 1]
                    }
    
    info_dict = {'1 Long layover'              : [1, 0, 0, 0, 0, 0, 0, 0, 0], 
                 '1 Short layover'             : [0, 1, 0, 0, 0, 0, 0, 0, 0], 
                 '2 Long layover'              : [0, 0, 1, 0, 0, 0, 0, 0, 0],
                 'Business class'              : [0, 0, 0, 1, 0, 0, 0, 0, 0],
                 'Change airports'             : [0, 0, 0, 0, 1, 0, 0, 0, 0],
                 'In-flight meal not included' : [0, 0, 0, 0, 0, 1, 0, 0, 0],
                 'No check-in baggage included': [0, 0, 0, 0, 0, 0, 1, 0, 0],
                 'No info'                     : [0, 0, 0, 0, 0, 0, 0, 1, 0],
                 'Red-eye flight'              : [0, 0, 0, 0, 0, 0, 0, 0, 1]
                 }

    encoded_result = []

    for i in result.values():
        if type(i) == int:
            encoded_result.append(i)
        elif type(i) == float:
            encoded_result.append(i)
        elif i in ['LCC', 'Full service', 'Full service premium economy', 'Full service business', 'Multiple carriers', 'Multiple carriers premium economy']:
            encoded_result.extend(airline_dict[i])
        elif i in ['No info', 'No check-in baggage included', 'In-flight meal not included', 'Business class', 'Change airports', 'Red-eye flight','1 Short layover', '1 Long layover', '2 Long layover']:
            encoded_result.extend(info_dict[i])

    single_array = np.array(encoded_result).reshape(1, -1)

    scaling = load_scaler("scaling.pkl")    
    scaling_array = scaling.transform(single_array)

    model = load_model("model.pkl")  
    prediction = model.predict(scaling_array)
    final_result = int(np.expm1(prediction[0]))

    st.success(f'The estimated ticket price for your flight is {final_result} INR')
    st.markdown('''<p style='text-align: justfy;'> <br> <strong>Disclaimer:</strong> This is an estimated price. The price may change over time due to several factors, such as the date of booking, flight demand, and other factors.</p>''', unsafe_allow_html=True)