from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import date,datetime
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
meetingCounter = 0


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abduqazi'
app.config['MYSQL_DB'] = 'shaheen'

# Intialize MySQL
mysql = MySQL(app)

# Global Varibales
counter = 0
charges= {}
charges['platinum'] = 250000
charges['gold'] = 150000
charges['silver'] = 100000
charges['gym'] = 700
charges['motor'] = 6000
charges['hitea'] = 2000
charges['swimming'] = 5000
charges['golf'] = 20000

"""
Function for basic login
"""
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
            session['m_type'] = account['subscription_type']
            session['cnic'] = account['cnic']
            session['amount'] = account['amount']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg = msg)

"""
Function for login of Board of Directors
"""
@app.route('/shaheen/BOD', methods=['GET', 'POST'])
def bodLogin():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        user = request.form['username']
        passw = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM bod WHERE username = %s AND password = %s', (user, passw,))
        # Fetch one record and return result
        account = cursor.fetchone()
         # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            session['id'] = account['bod_id']
            session['username'] = account['username']
            session['name'] = account['name']
            session['status'] = account['status']
            session['cnic'] = account['cnic']
            return redirect(url_for('bodHome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('bodLogin.html', msg = msg)

"""
Function for logout
"""
@app.route('/shaheen/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('name', None)
   # Redirect to login page
   return redirect(url_for('login'))

"""
Function for registering a member
"""
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
        m_since = date.today()
        d1 = m_since.strftime("%d/%m/%Y")
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
            m_status = 'pending'
            cursor.execute('INSERT INTO Members(name,username,password,email,cnic,dob,member_since,subscription_type,amount) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s,0)', ( name, user, passw, email, cnic, dob,d1, m_status))
            mysql.connection.commit()
            msg = 'Registration successful!'

    elif request.method == 'POST':
        msg = 'Fill out the form please.'

    return render_template('signup.html', msg=msg)

"""
Function for homepage of members
"""
@app.route('/shaheen/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', name = session['name'],  m_status = session['m_type'], amnt = session['amount'])
    else:
        return redirect(url_for('login'))

"""
Function for handling bookings of members
"""
@app.route('/shaheen/home/bookings', methods=['GET', 'POST'])
def bookings():
    msg = " "
    if 'loggedin' in session:
        if request.method == 'POST':
            b_type = request.form['ftype']
            money = charges[b_type]
            d = date.today()
            d1 = d.strftime("%d/%m/%Y")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            num_guests = int(request.form['guests'])
            msg = "Booking Successfull!"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO Booking(date,time,member_id,facility_type,facility_id,number_of_people,charges) Values(%s, %s, %s, %s, %s, %s, %s )',
                           (d1, current_time, session['id'], b_type,1,num_guests, money))
            cursor.execute(
                'SELECT booking_id from Booking WHERE(date = %s AND time=%s AND member_id=%s AND facility_type=%s AND facility_id=%s AND number_of_people=%s AND charges=%s) ',
                (d1, current_time, session['id'], b_type, 1, num_guests, money))
            booking= cursor.fetchone()
            session['booking_id'] = booking['booking_id']
            mysql.connection.commit()
            return redirect(url_for('receipt'))
        return render_template('bookings.html', msg = msg)
    else:
        return redirect(url_for('login'))

"""
Function for handling memberships of members
"""
@app.route('/shaheen/home/membership', methods=['GET', 'POST'])
def membership():
    if 'loggedin' in session:
        msg = " "
        if request.method == 'POST' and 'type' in request.form :
            msg = 'Membership Subscribed!'
            mem_type = request.form['type']
            session['m_type'] = mem_type
            if mem_type == 'platinum':
                charges = 250000
            if mem_type == 'gold':
                charges = 150000
            else:
                charges = 100000
            session['amount'] = charges
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE Members SET subscription_type = %s,amount = %s WHERE cnic = %s', (session['m_type'], charges, session['cnic']))
            mysql.connection.commit()
            return redirect(url_for('account'))
        return render_template('membership.html', msg = msg)
    else:
        return redirect(url_for('login'))

"""
Function for account details of members
"""
@app.route('/shaheen/home/account', methods=['GET', 'POST'])
def account():
    msg = ' '
    if 'loggedin' in session:
        if request.method == 'POST':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT subscription_type,amount FROM Members WHERE cnic = %s', [session['cnic']])
            account = cursor.fetchone()
            sub = account['subscription_type']
            money =   account['amount']
            money = money - charges[sub]
            if(money < 0):
                money = 0
            session['amount'] = money
            cursor.execute('UPDATE Members SET amount = %s WHERE cnic = %s',
                           (money, session['cnic']))
            mysql.connection.commit()
            msg = "Payment Processed! Enjoy the Rachna Exprience"
        return render_template('account.html', amnt = session['amount'], msg = msg)
    else:
        return redirect(url_for('login'))

"""
Function for generating receipts of payments
"""
@app.route('/shaheen/home/bookings/receipt', methods=['GET', 'POST'])
def receipt():
    msg = ' '
    purpose = ' '
    money = " "
    date1 = " "
    if 'loggedin' in session:
        d = date.today()
        d1 = d.strftime("%d/%m/%Y")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT facility_type,charges FROM Booking WHERE booking_id=%s',
            [session['booking_id']])
        account = cursor.fetchone()
        purpose = account['facility_type']
        money = account['charges']
        date1 = d1
        cursor.execute(
            'INSERT INTO Receipt(member_id,purpose,amount,date) VALUES ( %s, %s, %s, %s)',
            (session['id'], account['facility_type'], account['charges'], d1))
        if request.method == 'POST' and 'done' in request.form:
            msg = "Payment Successfull!"
        if request.method == 'POST' and 'notdone' in request.form:
            return redirect(url_for('bookings'))
        return render_template('receipt.html', msg = msg, purpose= purpose, money = money, date = date1 )
    else:
        return redirect(url_for('login'))

"""
Function for homepage of Board of Directors
"""
@app.route('/shaheen/bodHome', methods = ['GET', 'POST'])
def bodHome():
    if 'loggedin' in session:
        return render_template('bodHome.html', name = session['name'],  directorStatus = session['status'])
    else:
        return redirect(url_for('login'))

"""
Function for summary display for Board of Directors
"""
@app.route('/shaheen/bodHome/statAndSummary', methods = ['GET', 'POST'])
def statAndSummary():
    if 'loggedin' in session:
        return render_template('statAndSummary.html', name = session['name'],  directorStatus = session['status'])
    else:
        return redirect(url_for('login'))

"""
Function for meeting call for Board of Directors
"""
@app.route('/shaheen/bodHome/meeting', methods = ['GET', 'POST'])
def meeting():
    if 'loggedin' in session:
        global meetingCounter
        mssg = ''
        message = 'There are no meetings scheduled.'
        message1 = ''
        message2 = ''
        message3 = ''
        if meetingCounter > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM bodMeeting WHERE meeting_id=(SELECT max(meeting_id) FROM bodMeeting)')
            display = cursor.fetchone()
            message = display['bod_name'] + ' called a meeting.'
            message1 = 'Date : ' + display['date']
            message2 = 'Time : ' + display['time']
            message3 = 'Agenda : ' + display['agenda']
            mysql.connection.commit()
        if request.method == 'POST':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO bodMeeting (bod_name, time, date, agenda) VALUES (%s, %s, %s, %s)', (session['name'], request.form['time'], request.form['date'], request.form['agenda']))
            mysql.connection.commit()
            mssg = 'Meeting Called!'
            meetingCounter = meetingCounter + 1
        if meetingCounter > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM bodMeeting WHERE meeting_id=(SELECT max(meeting_id) FROM bodMeeting)')
            display = cursor.fetchone()
            message = display['bod_name'] + ' called a meeting.'
            message1 = 'Date : ' + display['date']
            message2 = 'Time : ' + display['time']
            message3 = 'Agenda : ' + display['agenda']
            mysql.connection.commit()
        return render_template('meeting.html', msg = mssg, message = message, message1 = message1, message2 = message2, message3 = message3)
    else:
        return redirect(url_for('login'))