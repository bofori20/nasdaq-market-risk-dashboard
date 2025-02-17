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
img_contact_form = Image.open("/Users/bryt/Desktop/MSDS/dstc691_capstone_applied_data_science/webpage/images/gradient.png")
img_lottie_animation = Image.open("/Users/bryt/Desktop/MSDS/dstc691_capstone_applied_data_science/webpage/images/IMG_3123.png")
img_contact_form1 = Image.open("/Users/bryt/Desktop/MSDS/dstc691_capstone_applied_data_science/webpage/images/download-3.png")
img_contact_form2 = Image.open("/Users/bryt/Desktop/MSDS/dstc691_capstone_applied_data_science/webpage/images/titanic.png")
img_contact_form3 = Image.open("/Users/bryt/Desktop/MSDS/dstc691_capstone_applied_data_science/webpage/images/nasdaq.png")
img_contact_form4 = Image.open("/Users/bryt/Desktop/MSDS/dstc691_capstone_applied_data_science/webpage/images/download-1.png")

# ------ BIOGRAPHICAL HOMEPAGE ------
     
with st.container():
    # Creating columns for centering the image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image(img_contact_form, width=1000)
#    st.image("img_contact_form", use_column_width=True)
    st.subheader("Welcome to My Data Science Capstone Project")
    st.write("""Hi there! I’m Bright Ofori, a data scientist passionate about transforming data into actionable
             insights and solutions. This webpage is the culmination of my journey through Masters in Data Science
             course, where I’ve applied my knowledge of data analysis, machine learning, and visualization 
             to tackle a real-world challenge.

            In this project, I explored stock price prediction leveraging 
            cutting-edge tools and techniques to uncover valuable insights. My work showcases the skills 
            I’ve developed, including:

            Data Wrangling and Preprocessing: Cleaning and preparing raw datasets for analysis.
            Exploratory Data Analysis: Identifying patterns and trends through visualization.
            Model Development and Evaluation: Building robust machine learning models.
            Storytelling with Data: Crafting compelling narratives to communicate findings.
            Feel free to explore the sections below to dive deeper into my methodology, findings, 
            and takeaways. Whether you're a fellow data enthusiast, recruiter, or simply curious, 
            I hope you find this project insightful and inspiring!
            """)
    # st.write("[Learn More >](https://mysock predictor.com)")
    
# ----- WHO I AM ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Who I am")
        st.write("##")
        st.write(
            """
            Academic Background:
            
            I am a strong believer in the power of data and I have cultivated 
            a strong foundation in Data Science through rigorous academic training.
            My education has focused on applied data science and artificical intelligence 
            complimented by practical experiences. These experiences have honed my analytical,
            problem-solving and collaborative skills.
            
            Career Aspirations:
            
            I aspire to be a Data Scientist who can lead impactful projects.
            I aim to work in environments that challenge me intellectually while allowing me to 
            make meaningful contributions. Ultimately, I seek to align my career path with opportunities 
            that improve lives and advance sustainable practices.
            
            Professional Interests:
            
            My professional interests include Machine Learning and healthcare innovation. 
            I am particularly drawn to green technology and growth trajectory of the data 
            science field. Additionally, I am passionate about fostering collaboration, 
            ethical practices and innovation in my field.
            
            Personal Introduction:
            
            Beyond academics and career pursuits, I enjoy hiking and playing cards. One unique aspect 
            of me is my ability to connect with diverse groups which has often helpe me develop tolerance 
            and a increased sense of result for all cultures. These activities not only balance 
            my professional life but also inspire creativity and resilience.
            
            """
        )
 #       st.write("[My Resume >](https://google.fjnskjnf.com)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
        
# ---- Resume Page ---- 
with st.container():
    st.write("---")
    st.header("My Resume")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img_lottie_animation)
    with text_column:
        st.subheader("Passionate about solving complex problems and contributing to impactful data-driven decisions in a fast-paced environment")
        st.header("Personal Details")
        st.write("**Name:** Bright Ofori")
        st.write("**Email:** bright.ofori.bo@gmail.com")
        st.write("**Phone:** +1(510)926-7406")
        st.write("**LinkedIn:** (https://linkedin.com/in/bright-ofori)")
        # st.write("**Portfolio/Website:** [Your Website](https://yourwebsite.com)")
        
        # Education Section
        st.header("Education")
        st.subheader("Master of Science in Data Science")
        st.write("**Institution:** Eastern University")
        st.write("**Years:** Completion - December 2024")
        
        st.subheader("MBA in Finance")
        st.write("**Institution:** Lincoln University")
        st.write("**Years:** 2013 - 2015")
        st.write("**Achievements:**")
        st.write("- Best Graduating Thesis")
        
        st.subheader("Bachelor of Arts in Psychology")
        st.write("**Institution:** University of Ghana")
        st.write("**Years:** 2002 - 2006")
        
        # Work Experience Section
        st.header("Work Experience")
        st.subheader("Residential Loan Administrator")
        st.write("**Company:** JP Morgan Chase")
        st.write("**Years:** July 2021 - August 2024")
        st.write("**Responsibilities:**")
        st.write("- Documents review and due diligence for loan closings.")
        st.write("- Coordinate with borrowers, escrow and funders on loan conditions.")
        
        st.subheader("Relationship Banker")
        st.write("**Company:** Union Bank")
        st.write("**Years:** January 2019 - July 2021")
        st.write("**Responsibilities:**")
        st.write("- Proactively assess clients' needs and recommend appropriate products")
        st.write("- Responsible for managing, retaining and growing book of business")

        # Footer
        st.write("---")
        st.write("Thank you for viewing my resume!")

 
#        st.markdown("[Watch video...](https://presentation video)")
# ---- General Page ---- 
with st.container():
    st.title("General Projects Page")

# Introduction
st.write("Welcome to my General Projects page! Here, you can explore some of the projects I have worked on.")

# Projects Section
st.header("Project: The titanic survival predictor")

# Project 1
st.write("A predictor of survival in the titanic considering age, sex and class of passengers")
# Creating columns for centering the image
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(img_contact_form2, width=700)

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

st.title("Titanic Survival Prediction")
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


# Add more projects as needed
st.write("---")
st.write("Thank you for exploring my project! Feel free to reach out if you have any questions or would like to collaborate.")


# Title
st.title("This Project")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image(img_contact_form3, width=1000)

# Problem Statement
st.header("Problem Being Addressed")
st.write("""
The primary goal of this project is to develop a machine learning model that predicts future stock prices 
based on historical stock data. It is also to gain a deeper understanding of the factors that influence 
stock market movements which ultimately will provide investors and traders with actionable insights that 
can enhance their decision-making processes in the stock market. The overarching goal is to create a 
reliable tool that can help mitigate investment risks and maximize returns.
""")

# Approach
st.header("Approach")
st.write("""
To address this problem, we applied a combination of data analysis, machine learning, and user-focused design. 
The process involved:
- Collecting and cleaning data to ensure accuracy.
- Building a predictive model using Long Short-Term Memory (LSTM).
- Designing an interactive tool that allows users to access the predictions easily.
""")

# Results
st.header("Results")
st.write("""
The solution has shown significant improvements in predictive accuracy. For example:
- Demonstrated reliable predictions for test datasets.
These results highlight the potential to support decision-making and improve efficiency for investors.
""")

# Interactive Model Section
st.header("Try the Model")
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

st.title("Stock Price Predictor App")

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


# ---- Contact Section ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    contact_form = """
    <form action="https://formsubmit.co/your_email@example.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
     </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()


