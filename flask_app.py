from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)
app.secret_key = '07dbf544095c87c7bde2e66ddcf30afaa4485414'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'M0@090304'
app.config['MYSQL_DB'] = 'user_database'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mohammedsiraj98345@gmail.com'  
app.config['MAIL_PASSWORD'] = 'dfeg djun ovbx fkcg' 
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']  # Use the same as MAIL_USERNAME

mysql = MySQL(app)
mail = Mail(app)


s = URLSafeTimedSerializer(app.secret_key)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email'] 
        dob = request.form['dob']  
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, email, dob) VALUES (%s, %s, %s, %s)", (username, hashed_password, email, dob))
        mysql.connection.commit()
        cur.close()

        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):  # Assuming user[2] is the password
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            email = user[0]  
            token = s.dumps(username, salt='password-reset-salt')
            link = url_for('reset_password', token=token, _external=True)

            msg = Message('Password Reset Request', recipients=[email]) 
            msg.body = f'Your password reset link is {link}'
            mail.send(msg)

            flash('An email has been sent with instructions to reset your password.')
            return redirect(url_for('login'))
        else:
            flash('Username not found.')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        username = s.loads(token, salt='password-reset-salt', max_age=3600) 
    except:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, username))
        mysql.connection.commit()
        cur.close()

        flash('Your password has been updated!')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/streamlit/<option>')
def streamlit_app(option):
    if 'user' in session:
        os.system(f"streamlit run streamlit_apps/{option}_app.py")
        return f"Streamlit app '{option}' is running..."
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
