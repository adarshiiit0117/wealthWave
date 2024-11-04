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
api_key = "1a9444f6065ad0fce6a13525442c3c8727c92868"  # Replace with your Tiingo API key
news_api_key = "aebf914e21f7429d8416bf02c269b305"  # Replace with your News API key

# Default start and end dates
default_start_date = '2023-10-16'
default_end_date = '2024-10-16'

# Streamlit app title
st.title('Gold Price Prediction and News Sentiment')

# User input for gold price data
ticker_symbol = "GOLD"  # Fixed for gold prices
url = f"https://api.tiingo.com/tiingo/daily/{ticker_symbol}/prices"

# Fetching gold price data from Tiingo API
params = {
    'startDate': default_start_date,
    'endDate': default_end_date,
    'token': api_key
}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # Process the data
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Plotting gold prices
    st.subheader(f"{ticker_symbol} Gold Prices Over Time")
    st.line_chart(df['close'])

    # Data preprocessing for model
    df2 = df[['close']].reset_index()
    scaler = MinMaxScaler()
    df2[['close']] = scaler.fit_transform(df2[['close']])

    # Train-test split
    train_size = int(len(df2) * 0.8)
    train, test = df2[:train_size], df2[train_size:]

    # Function to create dataset for LSTM
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

    # Define and train the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Predictions and model evaluation
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)
    train_mae = mean_absolute_error(y_train, train_predict)
    test_mae = mean_absolute_error(y_test, test_predict)

    # Predicting the next day's closing price
    def predict_next_day(model, last_data, time_step):
        last_data = last_data[-time_step:].reshape(1, time_step, 1)
        prediction = model.predict(last_data)
        return scaler.inverse_transform(prediction)

    last_closing_price = df2['close'].values[-time_step:]
    predicted_tomorrow = predict_next_day(model, last_closing_price, time_step)
    st.write(f'Predicted Closing Price for Tomorrow: ${predicted_tomorrow[0, 0]:.4f}')
else:
    st.error("Error fetching gold price data.")

# News API Integration
st.subheader(f"Latest News for {ticker_symbol} (Gold)")

# Function to fetch news
def get_news(ticker_symbol):
    news_url = f"https://newsapi.org/v2/everything?q=gold&sortBy=publishedAt&apiKey={news_api_key}"
    response = requests.get(news_url)
    if response.status_code == 200:
        news_data = response.json()
        return news_data['articles']
    else:
        st.error("Error fetching news data.")
        return []

# Display news articles with sentiment analysis
articles = get_news(ticker_symbol)
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
    st.write("No recent news articles found.")
