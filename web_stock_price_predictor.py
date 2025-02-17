# import streamlit as st    
import pandas as pd 
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import unicodedata
import re

# Function to clean unwanted characters from strings
def clean_value(value):
    if isinstance(value, str):
        value = unicodedata.normalize('NFKD', value)
        value = re.sub(r'[^\w\.\-]', '', value)
        value = value.strip()
    return value

def download_stock_data(stock_id):
    """Download historical stock data."""
    end = datetime.now()
    start = datetime(end.year - 10, end.month, end.day)
    data = yf.download(stock_id, start, end)
    return data

def calculate_moving_averages(data):
    """Calculate moving averages for the stock data."""
    data['MA_for_250_days'] = data['Close'].rolling(250).mean()
    data['MA_for_200_days'] = data['Close'].rolling(200).mean()
    data['MA_for_100_days'] = data['Close'].rolling(100).mean()
    return data

def prepare_data_for_prediction(data):
    """Prepare data for LSTM model prediction."""
    splitting_len = int(len(data) * 0.8)
    x_test = pd.DataFrame(data['Close'][splitting_len:])
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(x_test)

    x_data, y_data = [], []
    for i in range(100, len(scaled_data)):
        x_data.append(scaled_data[i - 100:i])
        y_data.append(scaled_data[i])

    return np.array(x_data), np.array(y_data), scaler, splitting_len

def load_model_and_predict(x_data, scaler):
    """Load the model and predict."""
    model = load_model("Latest_stock_price_model.keras")
    predictions = model.predict(x_data)
    inv_predictions = scaler.inverse_transform(predictions)
    return inv_predictions

def plot_graph(figsize, values, full_data, extra_data=0, extra_dataset=None):
    """Plot the graph with given data."""
    fig = plt.figure(figsize=figsize)
    plt.plot(values, 'Orange')
    plt.plot(full_data['Close'], 'b')
    if extra_data:
        plt.plot(extra_dataset)
    return fig

def compare_predictions(data, predictions, y_data, splitting_len, scaler):
    """Compare actual and predicted values."""
    inv_y_test = scaler.inverse_transform(y_data)
    plotting_data = pd.DataFrame(
        {
            'Original Test Data': inv_y_test.flatten(),
            'Predictions': predictions.flatten()
        },
        index=data.index[splitting_len + 100:]
    )
    return plotting_data



# st.title("Stock Price Predictor App")
# stock = st.text_input("Enter the Stock ID","NDX")

# model = load_model("Latest_stock_price_model.keras")
# st.subheader("Stock Data")
# st.write(nasdaq_data)

# splitting_len = int(len(nasdaq_data)*0.8)
# x_test = pd.DataFrame(nasdaq_data.Close[splitting_len:])

# def plot_graph(figsize, values, full_data, extra_data=0, extra_dataset = None):
#     fig = plt.figure(figsize=figsize)
#     plt.plot(values, 'Orange')
#     plt.plot(full_data.Close, 'b')
#     if extra_data:
#         plt.plot(extra_dataset)
#     return fig


# st.subheader('Original Close Price and MA for 250 days')
# nasdaq_data['MA_for_250_days'] = nasdaq_data.Close.rolling(250).mean()
# st.pyplot(plot_graph((15,6), nasdaq_data['MA_for_250_days'], nasdaq_data, 0))

# st.subheader('Original Close Price and MA for 200 days')
# nasdaq_data['MA_for_200_days'] = nasdaq_data.Close.rolling(200).mean()
# st.pyplot(plot_graph((15,6), nasdaq_data['MA_for_200_days'], nasdaq_data, 0))

# st.subheader('Original Close Price and MA for 100 days')
# nasdaq_data['MA_for_100_days'] = nasdaq_data.Close.rolling(100).mean()
# st.pyplot(plot_graph((15,6), nasdaq_data['MA_for_100_days'], nasdaq_data, 0))

# st.subheader('Original Close Price and MA for 100 days and MA for 250 days')
# st.pyplot(plot_graph((15,6), nasdaq_data['MA_for_100_days'], nasdaq_data,1, nasdaq_data['MA_for_250_days']))

# scaler = MinMaxScaler(feature_range=(0,1))
# scaled_data =scaler.fit_transform(x_test)
# #scaled_data = scaler.fit_transform(x_test[("Close", "NDX")].values.reshape(-1, 1))

# x_data = []
# y_data = []

# for i in range (100, len(scaled_data)):
#     x_data.append(scaled_data[i-100:i])
#     y_data.append(scaled_data[i])
    
# x_data, y_data = np.array(x_data), np.array(y_data)

# predictions = model.predict(x_data)

# inv_pre = scaler.inverse_transform(predictions)
# inv_y_test = scaler.inverse_transform(y_data)

# plotting_data = pd.DataFrame(
#   {
#    'original_test_data': inv_y_test.reshape(-1),
#       'predictions': inv_pre.reshape(-1)
#   },
#     index = nasdaq_data.index[splitting_len+100:]
# )
# st.subheader("Original values vs Predicted values")
# st.write(plotting_data)

# st.subheader ('Original Close Price vs Predicted Close Price')
# fig = plt.figure(figsize=(15,6))
# plt.plot(pd.concat([nasdaq_data.Close[:splitting_len+100], plotting_data] , axis=0))
# plt.legend(["Data- not used", "Original Test data", "Predicted Test data"])
# st.pyplot(fig)


    

