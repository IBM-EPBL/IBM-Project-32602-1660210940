#, uijekixtjmwophal

from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

from datetime import datetime


app = Flask(__name__)
var_list = []
var_list1 = []
app.secret_key='a'
conn= ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dxj24137;PWD=pGm0FgyMqS3Jy4JV",'','')

app.config['UPLOAD_FOLDER']  = os.path.join('static','pics')

@app.route('/')
@app.route('/loginpage',methods =['GET', 'POST'])
def loginpage():
    loginImg = os.path.join(app.config['UPLOAD_FOLDER'],'Plasma_login.png')
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            # return render_template('register.html', regImg=loginImg)
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username / password !'
            print("log")
    return render_template('login.html', msg = msg,loginImg=loginImg)


@app.route('/home')
def home():
    sql = "SELECT * FROM bank"
    stmt = ibm_db.exec_immediate(conn,sql)
    acnt = []
    abc = ibm_db.fetch_assoc(stmt)
    while abc!=False:
        account = abc
        acnt.append(account)
        abc = ibm_db.fetch_assoc(stmt)
    return render_template('Home.html',account=acnt)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    regImg = os.path.join(app.config['UPLOAD_FOLDER'],'Plasma_login.png')

    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        city = request.form['city']
        infect = request.form['infect']
        blood = request.form['blood']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        #else:
            # insert_sql = "INSERT INTO  users VALUES (?, ?, ?, ?, ?, ?, ?)"
            # prep_stmt = ibm_db.prepare(conn, insert_sql)
            # ibm_db.bind_param(prep_stmt, 1, username)
            # ibm_db.bind_param(prep_stmt, 2, email)
            # ibm_db.bind_param(prep_stmt, 3, phone_number)
            # ibm_db.bind_param(prep_stmt, 4, city)
            # ibm_db.bind_param(prep_stmt, 5, infect)
            # ibm_db.bind_param(prep_stmt, 6, blood)
            # ibm_db.bind_param(prep_stmt, 7, password)
            # ibm_db.execute(prep_stmt)
            # msg = 'You have successfully registered !'
            # return render_template('Home.html', msg = msg)
        else:

            var_list.append(username)
            var_list.append(email)
            var_list.append(phone_number)
            var_list.append(city)
            var_list.append(infect)
            var_list.append(blood)
            var_list.append(password)
            bodytemp = r"D:\\PDA-B6\\templates\\email.html"
            with open(bodytemp, "r", encoding='utf-8') as f:
                html= f.read()


            # Set up the email addresses and password. Please replace below with your email address and password
            email_from = 'deekshidhasa@gmail.com'
            epassword = 'uijekixtjmwophal'
            email_to = email

            # Generate today's date to be included in the email Subject
            date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

            # Create a MIMEMultipart class, and set up the From, To, Subject fields
            email_message = MIMEMultipart()
            email_message['From'] = email_from
            email_message['To'] = email_to
            email_message['Subject'] = f'Report email - {date_str}'

            # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
            email_message.attach(MIMEText(html, "html"))
            # Convert it as a string
            email_string = email_message.as_string()

            # Connect to the Gmail SMTP server and Send Email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email_from, epassword)
                server.sendmail(email_from, email_to, email_string)
            return render_template('notify.html')
            
    return render_template('register.html', msg = msg,regImg=regImg)
    
@app.route('/confirm')
def confirm():
   insert_sql = "INSERT INTO  users VALUES (?, ?, ?, ?, ?, ?, ?)"
   prep_stmt = ibm_db.prepare(conn, insert_sql)
   ibm_db.bind_param(prep_stmt, 1, var_list[0])
   ibm_db.bind_param(prep_stmt, 2, var_list[1])
   ibm_db.bind_param(prep_stmt, 3, var_list[2])
   ibm_db.bind_param(prep_stmt, 4, var_list[3])
   ibm_db.bind_param(prep_stmt, 5, var_list[4])
   ibm_db.bind_param(prep_stmt, 6, var_list[5])
   ibm_db.bind_param(prep_stmt, 7, var_list[6])
   ibm_db.execute(prep_stmt)
   return render_template('confirm.html')
 


@app.route('/requestpage')

def requestpage():
    return render_template('Request.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   regImg = os.path.join(app.config['UPLOAD_FOLDER'],'Plasma_login.png')
   return render_template('login.html',regImg=regImg)

@app.route('/display')
def display():
    name = request.args.get("name")
    sql = "SELECT * FROM "+name
    stmt = ibm_db.exec_immediate(conn,sql)
    acnt = []
    abc = ibm_db.fetch_assoc(stmt)
    while abc!=False:
        account = abc
        acnt.append(account)
        abc = ibm_db.fetch_assoc(stmt)
    return render_template('display.html',account=acnt)

@app.route('/alertmail', methods =['GET', 'POST'])
def alertmail():
    msg = ''
    if request.method == 'POST' :
        name = request.form['name']
        mail = request.form['mail']
        contact = request.form['contact']
        location = request.form['location']
        bloodgroup = request.form['bloodgroup']
        unit = request.form['unit']        
        var_list1.append(name)
        var_list1.append(mail)
        var_list1.append(contact)
        var_list1.append(location)
        var_list1.append(bloodgroup)
        var_list1.append(unit)

        if location == 'Government Headquarters Hospital,Tenkasi':
            var_list1.append('B1')
        elif location == 'Government Hospital, Sankarankovil':
            var_list1.append('B2')
        elif location == 'Government Hospital, Ambasamudram':
            var_list1.append('B3')
        elif location == 'Government Medical College Hospital, Tirunelveli':
            var_list1.append('B4')
        elif location == 'Government Headquarters Hospital, Kovilpatti':
            var_list1.append('B5')
        else:
            var_list1.append('B6')

        bodytemp = r"D:\\PDA-B6\\templates\\email1.html"
        with open(bodytemp, "r", encoding='utf-8') as f:
            html= f.read()


        # Set up the email addresses and password. Please replace below with your email address and password
        email_from = 'deekshidhasa@gmail.com'
        epassword = 'uijekixtjmwophal'
        email_to = mail

        # Generate today's date to be included in the email Subject
        date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

        # Create a MIMEMultipart class, and set up the From, To, Subject fields
        email_message = MIMEMultipart()
        email_message['From'] = email_from
        email_message['To'] = email_to
        email_message['Subject'] = f'Report email - {date_str}'

        # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
        email_message.attach(MIMEText(html, "html"))
        # Convert it as a string
        email_string = email_message.as_string()

        # Connect to the Gmail SMTP server and Send Email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email_from, epassword)
            server.sendmail(email_from, email_to, email_string)
        return render_template('notify1.html')
            
    
@app.route('/update')
def update():
   insert_sql = "UPDATE B1 SET UNITS - = ? WHERE BLOOD = ?"
   prep_stmt = ibm_db.prepare(conn, insert_sql)
   #ibm_db.bind_param(prep_stmt, 1, var_list1[6])
   ibm_db.bind_param(prep_stmt, 1, var_list1[5])
   ibm_db.bind_param(prep_stmt, 2, var_list1[4])
   print(var_list1[6])
   print(var_list1[5])
   print(var_list1[4])
   ibm_db.execute(prep_stmt)
   return render_template('home.html')

@app.route('/confirm1')
def confirm1():
    return render_template('confirm1.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0')
