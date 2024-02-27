from flask import Flask, render_template, request, session, redirect, flash
from pymongo import MongoClient
from backend.classes.database import DB

app = Flask(__name__)
# MongoDB setup
client = MongoClient("mongodb://admin:admin@mongodb:27017", connect=False)
db_name = client['APR2']
collection = db_name['QR_code']
db = DB(qr=db_name["QR_code"]) # pouziti docker mongo
#db = DB(users=collection_users, qr=collection)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('home.html')
#I'm gonna fucking kill myself
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        qr_code = request.form['qr_code']
        user = db.login_user(username, qr_code)
        if user:
            user_id = user["_id"]
            session['user_id'] = user_id
            flash('You are now logged in', 'Success')
            db.add_student(username, qr_code)
            return redirect('/')
        else:
            flash('Login unsuccessful. Please check username and qr_code', 'danger')
            return redirect('/about')
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host="0.0.0.0", port=5000, debug=True)
