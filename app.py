from PIL import Image
import requests
import streamlit as st 
from streamlit_lottie import st_lottie 

# Find more emojis here : https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
local_css("style/style.css")

# --- LOAD ASSETS -----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
img_contact_form = Image.open("images/gradient.png")
#img_lottie_animation = Image.open("images/IMG_3123.png")
img_contact_form1 = Image.open("images/download-3.png")
img_contact_form2 = Image.open("images/titanic.png")
img_contact_form3 = Image.open("images/nasdaq.png")
img_contact_form4 = Image.open("images/download-1.png")

# ------ BIOGRAPHICAL HOMEPAGE ------
     
with st.container():
    # Creating columns for centering the image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image(img_contact_form, width=1000)
#    st.image("img_contact_form", use_column_width=True)
    st.header("👋 Welcome!")
    st.write("""Welcome to my data science portfolio! Here, you’ll find practical projects that demonstrate my ability to 
             turn data into actionable insights. I invite you to explore two featured projects:

🚢 Titanic Survival Predictor – A classification model built with machine learning to predict 
passenger survival on the Titanic, demonstrating my proficiency in feature engineering, 
model interpretation, and building interactive web applications using Flask and Streamlit.

📈 Stock Price Predictor – A deep learning model that leverages historical financial data to forecast 
future stock prices, showcasing my skills in time-series analysis, data preprocessing, and model 
deployment using Streamlit.

These projects reflect my passion for solving real-world problems through data and highlight my technical
range—from data wrangling and model building to deploying interactive applications. Happy exploring!
            """)
    # st.write("[Learn More >](https://mysock predictor.com)")
    
# ----- PROJECTS ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("Projects")
        st.header("Project 1: Titanic Survival Predictor")

# Creating columns for centering the image
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(img_contact_form2, width=700)
st.subheader("Overview")
st.write( """
The Titanic Survival Predictor is a machine learning web application designed to predict 
the likelihood of survival for a passenger aboard the Titanic. Built as a classification problem, 
this project explores the use of supervised learning to draw meaningful insights from historical 
data and deliver real-time predictions through a user-friendly interface.
""")

st.subheader("Objectives")
st.write("""
Develop a predictive model to estimate survival chances based on key passenger attributes.
Demonstrate feature engineering, model selection, and evaluation skills.
Deploy an interactive web app using Flask and Streamlit for user engagement.
""")

st.subheader("Key Features")
st.write("""
User Inputs: Users provide inputs such as age, sex, and passenger class.
Preprocessing Pipeline: Inputs are encoded into features compatible with the trained model.
Prediction Output: The model outputs a survival probability, helping users understand how likely a passenger was to survive.
Model: A logistic regression or neural network model trained on the classic Titanic dataset from Kaggle.
""")

st.subheader("Highlights")
st.write("""
Feature Engineering: Transformed categorical variables like sex and passenger class into binary indicators.
Model Training: Achieved high accuracy through cross-validation and hyperparameter tuning.
Deployment: Two versions of the application were built—one using Flask for traditional web routing, and another 
with Streamlit for rapid prototyping and interactivity.
""")

st.subheader("Learning Outcomes")
st.write("""
Gained hands-on experience building classification models from end to end.
Learned to translate raw data into actionable predictions using machine learning.
Practiced deploying machine learning models as fully functional web apps.
Strengthened understanding of model interpretability and user-centric design.
""")
        
 #st.write("[My Resume >](https://google.fjnskjnf.com)")
#with right_column:
 #   st_lottie(lottie_coding, height=300, key="coding")
        
 
#        st.markdown("[Watch video...](https://presentation video)")
# Projects Section

import pandas as pd
import joblib

# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------- Helper Function ------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

def preprocess_data_and_predict(age, sex, pclass):
    # Define and instantiate the variables for the encoded columns
    sex_f = 0
    sex_m = 0
    pclass_1 = 0
    pclass_2 = 0
    pclass_3 = 0

    if sex == 'F':
        sex_f = 1
    else:
        sex_m = 1

    if pclass == '1':
        pclass_1 = 1
    elif pclass == '2':
        pclass_2 = 1
    else:
        pclass_3 = 1

    # Create the DataFrame for prediction
    data = pd.DataFrame({
        'Age': [age],
        'Sex_female': [sex_f],
        'Sex_male': [sex_m],
        'Pclass_1': [pclass_1],
        'Pclass_2': [pclass_2],
        'Pclass_3': [pclass_3]
    })

    # Load the trained model
    with open('titanic.pkl', 'rb') as file:
        trained_model = joblib.load(file)

    # Use the model to predict
    probability = trained_model.predict_proba(data)
    survival_probability = probability[0][1]
    return round(survival_probability * 100, 1)


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------- Streamlit Application ------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

st.subheader("Titanic Survival Prediction")
st.markdown("We trained a neural network to predict Titanic survival. Enter the passenger details below:")

# Input form
age = st.number_input("Age", min_value=0, max_value=100, step=1, value=30)
sex = st.selectbox("Sex", options=["M", "F"], index=0)
pclass = st.selectbox("Passenger Class", options=["1", "2", "3"], index=0)

if st.button("Predict Survival Probability"):
    try:
        survival_probability = preprocess_data_and_predict(age, sex, pclass)
        st.success(f"The model predicts a {survival_probability}% chance of survival.")
    except Exception as e:
        st.error(f"Error in prediction: {e}")


# Project 2
with st.container():
    st.write("---")
st.header("Project 2: Stock Price Predictor")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(img_contact_form3, width=1000)

# Problem Statement
st.subheader("Problem Being Addressed")
st.write("""
The primary goal of this project is to develop a machine learning model that predicts future stock prices 
based on historical stock data. It is also to gain a deeper understanding of the factors that influence 
stock market movements which ultimately will provide investors and traders with actionable insights that 
can enhance their decision-making processes in the stock market. The overarching goal is to create a 
reliable tool that can help mitigate investment risks and maximize returns.
""")

# Approach
st.subheader("Approach")
st.write("""
To address this problem, we applied a combination of data analysis, machine learning, and user-focused design. 
The process involved:
- Collecting and cleaning data to ensure accuracy.
- Building a predictive model using Long Short-Term Memory (LSTM).
- Designing an interactive tool that allows users to access the predictions easily.
""")

# Results
st.subheader("Results")
st.write("""
The solution has shown significant improvements in predictive accuracy. For example:
- Demonstrated reliable predictions for test datasets.
These results highlight the potential to support decision-making and improve efficiency for investors.
""")

# Interactive Model Section
st.subheader("Try the Model")
st.write("""
Use the interface below to interact with the deployed model. Provide the stock ID, and the model will generate predictions and analyses.
""")
from web_stock_price_predictor import (
    download_stock_data,
    calculate_moving_averages,
    prepare_data_for_prediction,
    load_model_and_predict,
    plot_graph,
    compare_predictions,
    clean_value
)
import matplotlib.pyplot as plt

st.subheader("Stock Price Predictor App")

# Input stock symbol
stock_id = st.text_input("Enter the Stock ID", "NDX")
stock_id = clean_value(stock_id)
st.write(f"Using Stock ID: {stock_id}")

# Button to load data and run predictions
if st.button("Load and Predict"):
    try:
        # Download stock data
        data = download_stock_data(stock_id)
        st.subheader("Stock Data")
        st.write(data)

        # Calculate moving averages
        data = calculate_moving_averages(data)

        # Plot moving averages
        st.subheader("Moving Averages")
        st.pyplot(plot_graph((15, 6), data['MA_for_250_days'], data))
        st.pyplot(plot_graph((15, 6), data['MA_for_200_days'], data))
        st.pyplot(plot_graph((15, 6), data['MA_for_100_days'], data))

        # Prepare data for prediction
        x_data, y_data, scaler, splitting_len = prepare_data_for_prediction(data)

        # Predict using the loaded model
        predictions = load_model_and_predict(x_data, scaler)

        # Compare predictions
        plotting_data = compare_predictions(data, predictions, y_data, splitting_len, scaler)
        st.subheader("Original vs Predicted Values")
        st.write(plotting_data)

        # Plot comparison
        st.subheader("Close Price: Original vs Predicted")
        fig = plt.figure(figsize=(15, 6))
        plt.plot(data['Close'][:splitting_len + 100], label="Data Not Used")
        plt.plot(plotting_data['Original Test Data'], label="Original Test Data")
        plt.plot(plotting_data['Predictions'], label="Predicted Data")
        plt.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        

# Creating columns for centering the text
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
st.write("Thank you for exploring my projects!")





