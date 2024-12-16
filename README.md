# MarketPulse

## Real-Time Prediction for Stock, Bitcoin, and Gold Prices

---

### Tech Stack

#### 1. Frontend & Frameworks
- **Streamlit**: For building interactive web applications, mainly for the user interface.
- **Flask**: Used for handling the login page functionality.

#### 2. APIs for Data Fetching
- **News API**: For fetching news data related to stocks, financial markets, or relevant topics.
- **Tiingo API**: For accessing financial market data, such as stock prices and cryptocurrency data.

#### 3. Database
- **MySQL**: Used for storing and managing data efficiently.

#### 4. Data Handling & Processing
- **Pandas**: For data manipulation and analysis.
- **NumPy**: For numerical computations and handling array structures.
- **TextBlob**: For performing sentiment analysis on news data, providing sentiment scores.

#### 5. Machine Learning & Data Scaling
- **Scikit-learn**: Specifically using `MinMaxScaler` for scaling features.
- **TensorFlow & Keras**:
  - LSTM (Long Short-Term Memory): A type of neural network layer used for time-series prediction.
  - Dropout: For preventing overfitting during model training.
  - Dense Layers: For building the structure of the neural network.

#### 6. Evaluation Metrics
- **Mean Absolute Error (MAE)**: To measure the accuracy of the predictions.

---

## Project Description

The Real-Time Prediction for Stock, Bitcoin, and Gold project is a Flask-based application that provides real-time price predictions and analysis for stocks, Bitcoin, and gold. Key features include:

1. **Real-Time Price Predictions**: Uses machine learning models (e.g., LSTM) to forecast prices for stocks, Bitcoin, and gold based on historical data.
2. **Technical Analysis**: Incorporates financial indicators to assist in understanding market trends and price movements.
3. **User Interface**: Provides a user-friendly interface built with Flask for easy navigation and interaction, making real-time financial data accessible.
4. **Streamlit Integration**: Runs specific prediction models via Streamlit for advanced visualization and interactive analysis.
5. **News Sentiment Analysis**: Integrates recent news articles and performs sentiment analysis to provide insights into factors affecting price trends for these assets.

---

## Flask Login and Registration Page

### 1. App Configuration
- Sets up Flask, MySQL, and Mail configurations. The MySQL configuration handles database interactions, while email settings are configured for sending password reset emails via Gmail.
- `secret_key` is set for secure session management, and a `URLSafeTimedSerializer` is initialized to create secure, time-sensitive tokens for password reset links.

### 2. User Authentication Routes
- **Home**: Redirects logged-in users to the dashboard; otherwise, it displays the login page.
- **Register**: Manages user registration. It collects a username, hashed password, email, and date of birth, then stores them in the database. A flash message confirms successful registration.
- **Login**: Checks if the entered username and password match any stored in the database. If correct, it logs the user in by creating a session, allowing access to the dashboard.
- **Logout**: Logs the user out by clearing their session.

### 3. Password Reset Functionality
- **Forgot Password**: Generates a password reset link if the user provides a valid username. The link, containing a secure token, is sent to the user’s email.
- **Reset Password**: This route verifies the reset token and allows the user to set a new password. If the token is valid, the password is updated in the database.

### 4. Dashboard and Streamlit Integration
- **Dashboard**: Only accessible to logged-in users, providing a personalized interface.
- **Streamlit Integration**: Allows a specific Streamlit app (based on the `option` parameter) to run directly from Flask. This integration facilitates running data visualization or machine learning models in a more interactive interface using Streamlit.

### 5. Error Handling and Flash Messages
- Flash messages notify users about registration, login success/failure, and password reset statuses. Invalid or expired tokens for password resets are also handled with flash messages.

### 6. Running the Application
- The application is run in debug mode, suitable for development, which allows for live reloading and detailed error messages.

---


![image](https://github.com/user-attachments/assets/9631e14c-818c-4530-b05b-d6853c9da9bb)
![image](https://github.com/user-attachments/assets/0d7f7542-a478-40f2-b6fb-3b92b767eb02)
![image](https://github.com/user-attachments/assets/1c1b4705-5a4c-4129-a225-c1f35d6da337)
![image](https://github.com/user-attachments/assets/d6f1d328-5f36-4ba2-9ac5-21d57a63fd0b)
![image](https://github.com/user-attachments/assets/8e53b3b4-3d5a-445b-8b2e-17a3f1bad832)




