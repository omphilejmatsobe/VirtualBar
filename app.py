#!/usr/bin/python3
"""
This is the code base for VirtualBar.
This module runs most of the program
and operates the important classes and
instructions.
"""
import mimetypes

from flask import Flask, render_template, request, redirect, session
from flask import url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'super user'
db = SQLAlchemy(app)


notes = []
calls = []


class UserDB(db.Model):
    """
    This initializes the database table and columns
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)

    img = db.Column(db.Text, unique=True, nullable=True)
    picname = db.Column(db.Text, unique=True, nullable=True)
    mimetype = db.Column(db.Text, unique=True, nullable=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This controls all the login features
    """

    message = ""

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserDB.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard',  username=user.username, email=user.email))
        else:
            message = "Account does't exist."
    return render_template('login/login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This controls all the signup features
    """

    message = ""
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = UserDB.query.filter((UserDB.username==username)|(UserDB.email==email)).first()

        if user:
            message = "Account Exists."
        else:
            hashed_password = generate_password_hash(password)
            newUser = UserDB(name=name, username=username, email=email, password=hashed_password)
            db.session.add(newUser)
            db.session.commit()

            return redirect('/login')

    return render_template('login/signup.html', message=message)


@app.route('/recover', methods=['POST'])
def passwordRecovery():
    """
    This controls all the account recovery features
    """

    if request.method == 'POST':
        email = request.form['email']

        user = UserDB.query.filter_by(email=email).first()
        if user:
            """
            send email for recovery
            """
            return redirect('/login')
        else:
            """
            flash that email does not exist and return to login
            """
            return redirect(url_for('login'))
    return render_template('login/recover.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    This controls dashboards features
    """

    user = UserDB.query.get(session['user_id'])

    if not user:
        return redirect(url_for('login'))

    if not user.img:
        default_img = True;

    return render_template('session/dashboard.html', logged_in=True, defaul_img=default_img, calls=calls, notes=notes, user=user)


@app.route('/session')
def sessionmeeting():
    """
    This displays the session page
    """
    user_online = UserDB.query.get(session['user_id'])
    return render_template('session/session.html', user_online=user_online)


@app.route('/call')
def call():
    """
    This displays the session page
    """
    user_online = UserDB.query.get(session['user_id'])
    return render_template('session/call.html', user_online=user_online)


@app.route('/join')
def join():
    return render_template('session/join.html')


@app.route('/logout')
def logout():
    return redirect( url_for('login'))


@app.route('/meeting')
def meeting():
    user_online = UserDB.query.get(session['user_id'])
    return render_template('session/meeting.html', logged_in=True, user_online=user_online)

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    user_online = UserDB.query.get(session['user_id'])

    default_img = True;

    if request.method == 'POST':
        user_online.username = request.form['name']
        user_online.username = request.form['username']

        default_img = False;
        db.session.add(user_online)
        db.session.commit()

    return render_template('session/profile.html', default_img=default_img, logged_in=True, user_online=user_online)


@app.route('/dashboard/addcall', methods=['POST'])
def addcall():

    name = request.form['name']
    description = request.form['description']
    time = request.form['time']
    type = request.form['type']
    calls.append({"name": name, "description" : description, "time" : time, "type" : type})
    return redirect(url_for('dashboard'))

@app.route('/dashboard/deletecall/<int:index>')
def deletecall(index):
    del calls[index]
    return redirect(url_for('dashboard'))

@app.route('/dashboard/<int:index>')
def deletenote(index):
    del notes[index]
    return redirect(url_for('dashboard'))

@app.route('/dashboard/addnote', methods=['POST'])
def addnote():
    note = request.form['note']
    notes.append({"note": note})
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
