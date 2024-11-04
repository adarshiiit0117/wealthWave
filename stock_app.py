# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_absolute_error, mean_squared_error

session_info = st.experimental_get_query_params().get('session')
st.set_page_config(page_title="Stock Price Prediction", page_icon="📈", layout="wide")

# Add some custom styles using Markdown
st.markdown(
    """
    <style>
        .main {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .sidebar {
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True
)

# Title of the app
st.title('Stock Price Prediction with LSTM')

# Sidebar for user input
with st.sidebar:
    st.header("User Input")
    ticker_symbol = st.text_input("Enter the stock ticker symbol", value="AAPL").lower()

# API Key and URL
api_key = "3a873b0ea1da63261a4981ccd3dd0f8c5a339da1"
url = "https://api.tiingo.com/tiingo/daily/aapl/prices"  # Default to Apple, will be updated based on user input

# Default start and end dates
default_start_date = '2023-10-16'
default_end_date = '2024-10-16'

# Fetching data from Tiingo API
params = {
    'startDate': default_start_date,
    'endDate': default_end_date,
    'token': api_key
}
response = requests.get(url.replace("aapl", ticker_symbol), params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # Process the data
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Plotting stock prices
    st.subheader(f"{ticker_symbol.upper()} Stock Prices Over Time")
    st.line_chart(df['close'])

    # Data preprocessing
    df2 = df[['close']].reset_index()
    scaler = MinMaxScaler()
    df2[['close']] = scaler.fit_transform(df2[['close']])

    # Train-test split
    train_size = int(len(df2) * 0.8)
    train, test = df2[:train_size], df2[train_size:]

    def create_dataset(data, time_step=1):
        X, y = [], []
        for i in range(len(data) - time_step - 1):
            a = data[i:(i + time_step), 0]
            X.append(a)
            y.append(data[i + time_step, 0])
        return np.array(X), np.array(y)

    time_step = 25
    X_train, y_train = create_dataset(train[['close']].values, time_step)
    X_test, y_test = create_dataset(test[['close']].values, time_step)

    # Reshape input to be [samples, time steps, features]
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Define and train the model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Predictions
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    # Calculate metrics
    train_mae = mean_absolute_error(y_train, train_predict)
    test_mae = mean_absolute_error(y_test, test_predict)

    # Predicting the next day
    def predict_next_day(model, last_data, time_step):
        last_data = last_data[-time_step:].reshape(1, time_step, 1)
        prediction = model.predict(last_data)
        return scaler.inverse_transform(prediction)

    last_closing_price = df2['close'].values[-time_step:]
    predicted_tomorrow = predict_next_day(model, last_closing_price, time_step)
    
    st.write(f'Predicted Closing Price for Tomorrow: **${predicted_tomorrow[0, 0]:.4f}**')
else:
    st.error(f"Error fetching data: {response.status_code}")
