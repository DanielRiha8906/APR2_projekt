from flask import Flask, render_template, request, session, redirect, flash, jsonify
from pymongo import MongoClient
from backend.classes.database import DB
import json

app = Flask(__name__)
# MongoDB setup
client = MongoClient("mongodb://admin:admin@mongodb:27017", connect=False)
db_name = client['APR2']
collection = db_name['QR_code']
db = DB(qr=db_name["QR_code"]) # pouziti docker mongo
#db = DB(users=collection_users, qr=collection)

#Prints out all students in a classroom
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        posts = db.qr.find({"Is_taken": {"$ne" :"0"}})
        return render_template('home.html', posts = posts)
@app.route('/about')
def about():
    return render_template('about.html')
# Is not an actual login -> asks for QR_code -> f Is_taken != 0 -> changes It_taken to username
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

# Endpoint to qr_code reads -> adding a student
@app.route('/guide', methods=["POST"])
def api_post_endpoint():
    student_qr_code = request.get_json()
    if student_qr_code:
        student_loads_qr_code = db.login_user(student_qr_code["user"], student_qr_code["qr_code"])
        if student_loads_qr_code == None:
            #QR_code does not exist
            return "does not exist", 404
        elif student_loads_qr_code:
            #It works as intended
            return "success", 200
        else:
            #QR_code exists but is occupied
            return "unauthorized", 402
    else:
        #Internal server issue
        return "failure", 500

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host="0.0.0.0", port=5000, debug=True)
