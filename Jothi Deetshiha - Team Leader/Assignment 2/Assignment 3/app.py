from urllib import request
from flask import Flask,request,render_template
app=Flask(__name__)


@app.route('/')
def index():
    return render_template('Registration.html')


@app.route('/success',methods=['POST'])
def home():
    name  = request.form.get("fname")
    return "<h1>Hello</h1>"+name+" how are you?"

if __name__=='__main__':
    app.run(debug=True)