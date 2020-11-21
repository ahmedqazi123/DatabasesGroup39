from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abduqazi'
app.config['MYSQL_DB'] = 'shaheen'

# Intialize MySQL
mysql = MySQL(app)

counter = 0


@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        user = request.form['username']
        passw = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Members WHERE username = %s AND password = %s', (user, passw,))
        # Fetch one record and return result
        account = cursor.fetchone()
         # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            session['id'] = account['member_id']
            session['username'] = account['username']
            session['name'] = account['name']
            return redirect(url_for('home'))

        else:
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg = msg)

@app.route('/shaheen/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('name', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/shaheen/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        user = request.form['username']
        passw = request.form['password']
        email = request.form['email']
        cnic = request.form['cnic']
        dob = request.form['dob']
        name = request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Members WHERE username = %s', (user,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'

        elif not re.match(r'[A-Za-z0-9]+', user):
            msg = 'Username must contain only characters and numbers!'

        elif not user or not passw or not email:
            msg = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO Members VALUES (NULL, %s, %s, %s, %s, %s, %s, 123, 123)', (name, user, passw, email, cnic, dob,))
            mysql.connection.commit()
            msg = 'Registration successful!'

    elif request.method == 'POST':
        msg = 'Fill out the form please.'

    return render_template('signup.html', msg=msg)

@app.route('/shaheen/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', name = session['name'])
    else:
        return redirect(url_for('login'))