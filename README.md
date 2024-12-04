PROJECT DESCRIPTION
The Real-Time Prediction for Stock, Bitcoin, and Gold project is a Flask-based application that provides real-time price predictions and analysis for stocks, Bitcoin, and gold. Key features include:
1.	Real-Time Price Predictions: Uses machine learning models (e.g., LSTM) to forecast prices for stocks, Bitcoin, and gold based on historical data.
2.	Technical Analysis: Incorporates financial indicators to assist in understanding market trends and price movements.
3.	User Interface: Provides a user-friendly interface built with Flask for easy navigation and interaction, making real-time financial data accessible.
4.	Streamlit Integration: Runs specific prediction models via Streamlit for advanced visualization and interactive analysis.
5.	News Sentiment Analysis: Integrates recent news articles and performs sentiment analysis to provide insights into factors affecting price trends for these assets.

FLASK LOGIN, registration PAGE CODE EXPALANATION
1-  App Configuration:
•	Sets up Flask, MySQL, and Mail configurations. The MySQL configuration handles database interactions, while email settings are configured for sending password reset emails via Gmail.
•	secret_key is set for secure session management, and a URLSafeTimedSerializer is initialized to create secure, time-sensitive tokens for password reset links.
2-  User Authentication Routes:
•	Home: Redirects logged-in users to the dashboard; otherwise, it displays the login page.
•	Register: Manages user registration. It collects a username, hashed password, email, and date of birth, then stores them in the database. A flash message confirms successful registration.
•	Login: Checks if the entered username and password match any stored in the database. If correct, it logs the user in by creating a session, allowing access to the dashboard.
•	Logout: Logs the user out by clearing their session.
3- Password Reset Functionality:
•	Forgot Password: Generates a password reset link if the user provides a valid username. The link, containing a secure token, is sent to the user’s email.
•	Reset Password: This route verifies the reset token and allows the user to set a new password. If the token is valid, the password is updated in the database.
4- Dashboard and Streamlit Integration:
•	Dashboard: Only accessible to logged-in users, providing a personalized interface.
•	Streamlit Integration: Allows a specific Streamlit app (based on the option parameter) to run directly from Flask. This integration facilitates running data visualization or machine learning models in a more interactive interface using Streamlit.
4- Error Handling and Flash Messages:
•	Flash messages notify users about registration, login success/failure, and password reset statuses. Invalid or expired tokens for password resets are also handled with flash messages.
5- Running the Application:
•	The application is run in debug mode, suitable for development, which allows for live reloading and detailed error messages. 
