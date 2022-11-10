#,
from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
import os

app = Flask(__name__)
app.secret_key='a'
conn= ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dxj24137;PWD=pGm0FgyMqS3Jy4JV",'','')

app.config['UPLOAD_FOLDER']  = os.path.join('static','pics')
   

   
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
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, phone_number)
            ibm_db.bind_param(prep_stmt, 4, city)
            ibm_db.bind_param(prep_stmt, 5, infect)
            ibm_db.bind_param(prep_stmt, 6, blood)
            ibm_db.bind_param(prep_stmt, 7, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('dashboard.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg,regImg=regImg)
    
if __name__ == '__main__':
   app.run(host='0.0.0.0')

