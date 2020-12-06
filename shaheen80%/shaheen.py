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
verified = False

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
        print("HERERERE")
        # Create variables for easy access
        user = request.form['username']
        passw = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM bod WHERE username = %s AND password = %s', (user, passw,))
        # Fetch one record and return result
        account = cursor.fetchone()
         # If account exists in accounts table in out database
        print("Here")
        if account:
            print("here")
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

@app.route('/shaheen/emp_login', methods=['GET', 'POST'])
def emp_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        user = request.form['username']
        passw = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Employee WHERE name = %s AND password = %s', (user, passw,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            session['loggedin'] = True
            session['id'] = account['employee_id']
            session['name'] = account['name']
            session['designation'] = account['designation']
            session['grade_no'] = account['grade_no']
            session['amount_owed'] = account['amount_owed']
            session['no_of_leaves'] = account['no_of_leaves']
            if account['designation'] == 'staff':
                return redirect(url_for('emp_home'))
            elif account['designation'] == 'finance':
                return redirect(url_for('financeHome'))
            elif account['designation'] == 'manager':
                return redirect(url_for('mg_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('emp_login.html', msg=msg)

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
    msg = ""
    message = ""
    message1 = ""
    message2 = ""
    message3 = ""
    message4 = ""
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS rowCount FROM Booking WHERE member_id = %s', [session['id']])
        row = cursor.fetchone()
        mysql.connection.commit()
        rowCount = row['rowCount']
        if rowCount > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Booking WHERE member_id = %s', [session['id']])
            row = cursor.fetchone()
            mysql.connection.commit()
            message = row['booking_id']
            message1 = row['facility_type']
            message2 = row['date']
            message3 = row['time']
            message4 = row['status']
        if request.method == 'POST':
            b_type = request.form['ftype']
            money = charges[b_type]
            d = date.today()
            d1 = d.strftime("%d/%m/%Y")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            num_guests = int(request.form['guests'])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO Booking(date,time,member_id,facility_type,facility_id,number_of_people,charges, status) Values(%s, %s, %s, %s, %s, %s, %s, %s)', (d1, current_time, session['id'], b_type,1,num_guests, money, 'Pending'))
            cursor.execute('SELECT booking_id from Booking WHERE(date = %s AND time=%s AND member_id=%s AND facility_type=%s AND facility_id=%s AND number_of_people=%s AND charges=%s) ', (d1, current_time, session['id'], b_type, 1, num_guests, money))
            booking= cursor.fetchone()
            session['booking_id'] = booking['booking_id']
            mysql.connection.commit()
            return redirect(url_for('receipt'))
        return render_template('bookings.html', msg = msg, message = message, message1 = message1, message2 = message2, message3 = message3, message4 = message4)
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
        cursor.execute('SELECT facility_type,charges FROM Booking WHERE booking_id=%s', [session['booking_id']])
        account = cursor.fetchone()
        purpose = account['facility_type']
        money = account['charges']
        date1 = d1
        cursor.execute('INSERT INTO Receipt(member_id,purpose,amount,date) VALUES ( %s, %s, %s, %s)', (session['id'], account['facility_type'], account['charges'], d1))
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

@app.route('/shaheen/emp_home', methods = ['GET', 'POST'])
def emp_home():
    if 'loggedin' in session:
        return render_template('emp_home.html', name = session['name'])
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

@app.route('/shaheen/emp_home/req_leave', methods = ['GET', 'POST'])
def req_leave():
    msg = ""
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT no_of_leaves FROM Employee WHERE employee_id=%s', [session['id']])
        mysql.connection.commit()
        display = cursor.fetchone()
        leaves = display['no_of_leaves']
        msg2 = "Number of leaves left " + str(leaves)
        print("Have left leaves", leaves)
        if (int(leaves) <= 0):
            msg = "You have already taken max number of leaves allowed this year."
            return render_template('req_leave.html', msg = msg, msg2 = msg2)
        if request.method == "POST":
            if int(leaves) - int(request.form['days']) < 0:
                print("more leaves")
                msg = "You cannot take more than 25 leaves."
            else:
                print("hereeeeee")
                leaves = int(leaves) - int(request.form['days'])
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE Employee SET no_of_leaves = %s WHERE employee_id=%s', (leaves, session['id']))
                mysql.connection.commit()
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT no_of_leaves FROM Employee WHERE employee_id=%s', [session['id']])
                mysql.connection.commit()
                leavesleft = cursor.fetchone()
                msg = "Leave granted!"
                msg2 = "Number of leaves left " + str(leavesleft['no_of_leaves'])
                return render_template('req_leave.html', msg = msg, msg2 = msg2)
        print("end")
        return render_template('req_leave.html', msg = msg, msg2 = msg2)
    else:
        return redirect(url_for('login'))


    
@app.route('/shaheen/emp_home/emp_eval', methods = ['GET', 'POST'])
def emp_eval():
    msg = ""
    msg1 = ""
    msg2 = ""
    msg3 = ""
    msg4 = ""
    msg5 = ""
    msg6 = ""
    msg7 = ""
    msg8 = ""
    msg9 = ""


    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT quart_report FROM Employee WHERE employee_id=%s', [session['id']])
        mysql.connection.commit()
        display = cursor.fetchone()
        if(display['quart_report'] == 'none'):
            msg = "your evaluation is not yet available"
        if request.method == 'POST' or display['quart_report'] == 'pending':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE Employee SET quart_report= %s WHERE employee_id=%s', ['pending', session['id']])
            mysql.connection.commit()
            msg = "Evaluation Requested"
        if display['quart_report'] == 'sent':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT*FROM Report WHERE emp_id=%s', [session['id']])
            evaluation = cursor.fetchone()
            mysql.connection.commit()
            msg1 = evaluation['emp_id']
            msg2 = evaluation['name']
            msg3 = evaluation['manager']
            msg4 = evaluation['date']
            msg5 = evaluation['job_knowledge']
            msg6 = evaluation['work_quality']
            msg7 = evaluation['attend']
            msg8 = evaluation['comm skills']
            msg9 = evaluation['initiative']
            #print(f'report : {msg1}\n {msg2}\n {msg3}\n {msg4}\n {msg5}\n {msg6}\n {msg7}\n {msg8}\n {msg9}\n')



            msg = "Evaluation obtained"


        return render_template('emp_eval.html', name = session['name'], msg= msg,msg1= msg1, msg2=msg2,msg3=msg3,msg4=msg4,msg5=msg5, msg6=msg6,msg7=msg7,msg8=msg8,msg9=msg9 )
    else:
        return redirect(url_for('login'))

@app.route('/shaheen/emp_home/req_loan', methods = ['GET', 'POST'])
def req_loan():
    msg = " "
    status = "Pending"
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT amount_owed FROM Employee WHERE employee_id=%s', [session['id']])
        mysql.connection.commit()
        display = cursor.fetchone()
        owed = display['amount_owed']
        if (int(owed) > 0):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Loan WHERE employeeID = %s', [session['id']])
            row = cursor.fetchone()
            mysql.connection.commit()
            return render_template('no_loan.html', message1 = row['employeeID'], message2 = row['amount'], message3 = row['reason'], message4 = row['status'])
        if request.method == 'POST':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT bank_account FROM Employee WHERE employee_id=(%s)',
                           [session['id']])
            mysql.connection.commit()
            display = cursor.fetchone()
            account_exists = display['bank_account']
            if(account_exists == None):
                msg = "Please verify account first!"
            else:
                amount_requested = request.form['amount']
                duration = request.form['time']
                reason = request.form['reason']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT max_loan FROM Grade WHERE grade_no=(SELECT grade_no FROM Employee WHERE employee_id=%s)', [session['id']])
                mysql.connection.commit()
                display = cursor.fetchone()
                if(int(amount_requested)>display['max_loan'] ):
                    msg = "Loan cannot be greater than annual salary!"
                else:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    amnt = int(amount_requested)
                    cursor.execute('UPDATE Employee SET amount_owed = %s WHERE employee_id=%s', (amount_requested, session['id']))
                    cursor.execute('INSERT INTO Loan (amount, employeeID, reason, duration, status) VALUES (%s, %s, %s, %s, %s)', (amount_requested, session['id'], reason, duration, status))
                    mysql.connection.commit()
                    msg = "Application sent!"
                    return render_template('app_sent.html')
        return render_template('req_loan.html', msg = msg)
    else:
        return redirect(url_for('login'))

@app.route('/shaheen/emp_home/verify_account', methods = ['GET', 'POST'])
def verify_account():
    global verified
    msg = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT bank_account FROM Employee WHERE employee_id=%s',
                   [session['id']])
    mysql.connection.commit()
    display = cursor.fetchone()
    if 'loggedin' in session:
        if(display['bank_account']):
            return render_template("verified.html")

        elif request.method == 'POST':
            ibn = request.form['account']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE Employee SET bank_account = %s WHERE employee_id=%s',
                           [ibn, session['id']])
            mysql.connection.commit()
            return render_template("verified.html")
        return render_template('verify_account.html',msg = msg)

@app.route('/shaheen/financeHome', methods = ['GET', 'POST'])
def financeHome():
    if 'loggedin' in session:
        return render_template('financeHome.html')
    else:
        return redirect(url_for('login'))
@app.route('/shaheen/mg_home', methods = ['GET', 'POST'])
def mg_home():
    if 'loggedin' in session:
        return render_template('mg_home.html', name = session['name'])
    else:
        return redirect(url_for('login'))

@app.route('/shaheen/mg_home/mg_eval', methods = ['GET', 'POST'])
def mg_eval():
    message = 'No pending evaluations.'
    message1 = ''
    message2 = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS rowCount FROM Employee WHERE quart_report = %s', ['pending'])
        display = cursor.fetchone()
        rowCount = display['rowCount']
        mysql.connection.commit()
        print(f'row count is {rowCount}')
        if rowCount != 0:
            print("here")
            message = "There are " + str(display['rowCount']) + " pending evaluations."
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Employee WHERE quart_report = %s', ['pending'])
            row = cursor.fetchone()
            mysql.connection.commit()
            message1 = row['employee_id']
            message2 = row['name']
        if request.method == 'POST':
            knowledge = request.form['job_k']
            work = request.form['work']
            attendance = request.form['att']
            init = request.form['in']
            com = request.form['com']
            d = date.today()
            d1 = d.strftime("%d/%m/%Y")


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE Employee SET quart_report = %s WHERE employee_id = %s',
                          ('sent', row['employee_id']))
            mysql.connection.commit()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO Report VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (row["employee_id"], row['name'],session['name'], d1,knowledge,work,attendance,init,com))
            mysql.connection.commit()
            return redirect(url_for('mg_eval'))

        return render_template('mg_eval.html', message = message, msg1 = message1, msg2= message2)
    else:
        return redirect(url_for('login'))

@app.route('/shaheen/financeHome/disperseSalary', methods = ['GET', 'POST'])
def disperseSalary():
    message = ""
    message1 = ""
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT SUM(amount) from Grade INNER JOIN Employee ON Grade.grade_no = Employee.grade_no")
        display = cursor.fetchone()
        mysql.connection.commit()
        if request.method == 'POST':
            amount = display['SUM(amount)']
            message = "Salaries Dispersed! "
            message1 = "Amount dispersed = " + str(amount)

            ''''' Uncomment after finance table is made
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT funds_available from Finance")
            funds_available = cursor.fetchone()
            mysql.connection.commit()
            funds_available = funds_available - amount
            funds_spent = funds_spent + amount

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE Finance SET funds_available = %s where year = 2020", funds_available)
            funds_available = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE Finance SET funds_spent = %s where year = 2020", funds_spent)
            funds_available = cursor.fetchone()
            mysql.connection.commit()'''''

        return render_template('disperseSalary.html', message = message, message1 = message1)
    else:
        return redirect(url_for('login'))

@app.route('/shaheen/financeHome/financeLoan', methods = ['GET', 'POST'])
def financeLoan():
    message = 'No active applications.'
    message1 = ''
    message2 = ''
    message3 = ''
    message4 = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS rowCount FROM Loan WHERE status = %s', ['Pending'])
        display = cursor.fetchone()
        rowCount = display['rowCount']
        mysql.connection.commit()
        if rowCount != 0:
            message = "There are " + str(display['rowCount']) + " pending applications."
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Loan WHERE status = %s', ['Pending'])
            row = cursor.fetchone()
            mysql.connection.commit()
            message1 = row['employeeID']
            message2 = row['amount']
            message3 = row['reason']
            message4 = row['duration']
            if request.method == 'POST':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE Loan SET status = %s WHERE employeeID = %s', (request.form['status'], row['employeeID']))
                mysql.connection.commit()
                return redirect(url_for('financeLoan'))
        else:
            message = 'No active applications.'
            message1 = ''
            message2 = ''
            message3 = ''
            message4 = ''
        return render_template('financeLoan.html', message = message, message1 = message1, message2 = message2, message3 = message3, message4 = message4)
    else:
        return redirect(url_for('login'))

@app.route('/shaheen/financeHome/financePayment', methods = ['GET', 'POST'])
def financePayment():
    msg = 'No active payments.'
    message = ''
    message1 = ''
    message2 = ''
    message3 = ''
    message4 = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS rowCount FROM Booking WHERE status = %s', ['Pending'])
        display = cursor.fetchone()
        rowCount = display['rowCount']
        mysql.connection.commit()
        if rowCount != 0:
            msg = "There are " + str(display['rowCount']) + " pending payments."
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Booking WHERE status = %s', ['Pending'])
            row = cursor.fetchone()
            mysql.connection.commit()
            message = row['booking_id']
            message1 = row['facility_type']
            message2 = row['date']
            message3 = row['time']
            message4 = row['status']
            if request.method == 'POST':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE Booking SET status = %s WHERE member_id = %s', (request.form['status'], row['member_id']))
                mysql.connection.commit()
                return redirect(url_for('financePayment'))
        else:
            msg = 'No active payments.'
            message = ''
            message1 = ''
            message2 = ''
            message3 = ''
            message4 = ''
        return render_template('financePayment.html', msg = msg, message = message, message1 = message1, message2 = message2, message3 = message3, message4 = message4)
    else:
        return redirect(url_for('login'))