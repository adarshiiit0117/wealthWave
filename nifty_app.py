# nifty_app.py

# Imports
import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_absolute_error
from textblob import TextBlob

# API Key configurations
tiingo_api_key = "1a9444f6065ad0fce6a13525442c3c8727c92868"  # Replace with your Tiingo API key
news_api_key = "aebf914e21f7429d8416bf02c269b305"  # Replace with your News API key

# Default start and end dates
default_start_date = '2023-10-16'
default_end_date = '2024-10-16'

# Streamlit app title
st.title('Nifty Index Prediction with News Sentiment')

# Function to fetch data from Tiingo API
def fetch_data(url, params):
    st.write(f"Fetching data from: {url} with params: {params}")  # Debugging info
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error fetching data from Tiingo API: {response.status_code} - {response.text}")
        return None


# Nifty 50 Prediction
st.header('Nifty 50 Index Prediction')
nifty_url = "https://api.tiingo.com/tiingo/daily/NSE:NIFTY/prices"
nifty_params = {'startDate': default_start_date, 'endDate': default_end_date, 'token': tiingo_api_key}
nifty_df = fetch_data(nifty_url, nifty_params)

if nifty_df is not None:
    nifty_df['date'] = pd.to_datetime(nifty_df['date'])
    nifty_df.set_index('date', inplace=True)
    
    # Plotting Nifty prices
    st.subheader('Nifty 50 Index Prices Over Time')
    st.line_chart(nifty_df['close'])

    # Data preprocessing for Nifty
    scaler = MinMaxScaler()
    nifty_scaled = scaler.fit_transform(nifty_df[['close']])

    # Train-test split
    train_size = int(len(nifty_scaled) * 0.8)
    train, test = nifty_scaled[:train_size], nifty_scaled[train_size:]

    # Create dataset for LSTM
    def create_dataset(data, time_step=1):
        X, y = [], []
        for i in range(len(data) - time_step - 1):
            a = data[i:(i + time_step), 0]
            X.append(a)
            y.append(data[i + time_step, 0])
        return np.array(X), np.array(y)

    time_step = 25
    X_train, y_train = create_dataset(train, time_step)
    X_test, y_test = create_dataset(test, time_step)

    # Reshape input to be [samples, time steps, features]
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Define and train the LSTM model for Nifty
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Function to predict the next day’s closing price
    def predict_next_day(model, last_data, time_step):
        last_data = last_data[-time_step:].reshape(1, time_step, 1)
        prediction = model.predict(last_data)
        return scaler.inverse_transform(prediction)

    # Predicting the next day's closing price
    last_closing_price_nifty = nifty_scaled[-time_step:]
    predicted_nifty_tomorrow = predict_next_day(model, last_closing_price_nifty, time_step)
    st.write(f'Predicted Closing Price for Nifty 50 Tomorrow: ₹{predicted_nifty_tomorrow[0, 0]:.2f}')

# Nifty 100 Prediction
st.header('Nifty 100 Index Prediction')
nifty100_url = "https://api.tiingo.com/tiingo/daily/NSE:NIFTY100/prices"
nifty100_params = {'startDate': default_start_date, 'endDate': default_end_date, 'token': tiingo_api_key}
nifty100_df = fetch_data(nifty100_url, nifty100_params)

if nifty100_df is not None:
    nifty100_df['date'] = pd.to_datetime(nifty100_df['date'])
    nifty100_df.set_index('date', inplace=True)
    
    # Plotting Nifty 100 prices
    st.subheader('Nifty 100 Index Prices Over Time')
    st.line_chart(nifty100_df['close'])

    # Data preprocessing for Nifty 100
    scaler = MinMaxScaler()
    nifty100_scaled = scaler.fit_transform(nifty100_df[['close']])

    # Train-test split
    train_size = int(len(nifty100_scaled) * 0.8)
    train, test = nifty100_scaled[:train_size], nifty100_scaled[train_size:]

    # Create dataset for LSTM
    X_train, y_train = create_dataset(train, time_step)
    X_test, y_test = create_dataset(test, time_step)

    # Reshape input to be [samples, time steps, features]
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Define and train the LSTM model for Nifty 100
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Predicting the next day's closing price for Nifty 100
    last_closing_price_nifty100 = nifty100_scaled[-time_step:]
    predicted_nifty100_tomorrow = predict_next_day(model, last_closing_price_nifty100, time_step)
    st.write(f'Predicted Closing Price for Nifty 100 Tomorrow: ₹{predicted_nifty100_tomorrow[0, 0]:.2f}')

# News API Integration
st.subheader('Latest News on Nifty Indices')

# Function to fetch news
def get_news(query):
    news_url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={news_api_key}"
    response = requests.get(news_url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        st.error("Error fetching news data.")
        return []

# Fetch and display news for Nifty
articles = get_news("Nifty 50 OR Nifty 100")
if articles:
    for article in articles[:5]:  # Limit to 5 recent articles
        title = article['title']
        description = article['description']
        url = article['url']
        published_date = article['publishedAt']

        # Perform sentiment analysis on the article's title and description
        sentiment = TextBlob(description if description else title).sentiment
        sentiment_score = "Positive" if sentiment.polarity > 0 else "Negative" if sentiment.polarity < 0 else "Neutral"

        # Display news details
        st.markdown(f"**[{title}]({url})**")
        st.write(f"Published on: {published_date}")
        st.write(f"Sentiment: {sentiment_score}")
        st.write(description)
        st.write("---")
else:
    st.error("No news articles found.")
