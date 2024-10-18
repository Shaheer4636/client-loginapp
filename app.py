from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to something secure

# SQL Server connection details
server = 'basic-login-app-upc-server.database.windows.net'
database = 'basic-login-app-upc-database'
username = 'basic-login-app-upc-server-admin'
password = 'your_password'  # Replace with your actual password
driver = '{ODBC Driver 17 for SQL Server}'  # Ensure this driver is installed

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model (adjust fields to match your DB structure)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords in production

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Query database to check if user exists
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    return f'Welcome, {session["username"]}!'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
