#!/usr/bin/python3

"""
This is the code base for VirtualBar.
This module runs most of the program
and operates the important classes and
instructions.
"""

from flask import Flask, render_template, request, redirect, session
from flask import url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'super user'
db = SQLAlchemy(app)


class UserDB(db.Model):
    id = sb.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Coilumn(db.Text, unique=True, nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = UserDB.query.filter_by(email=email, password=password).first()

        if user and check_password_hash(user.password, password):
            session['user id'] = user.id
            return redirect('/session')
        else:
            return redirect('/login')

    return render_template('login/login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

    return render_template('login/signup.html')


@app.route('/recover', methods=['POST'])
def passwordRecovery():
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
            return redirect('/login')
    return render_templater('login/recover.html')


@app.route('/session', methods=['GET', 'POST'])
def session():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('session/session.html', logged_in=True)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile/profile.html')


if __name__ == '__main__':
    app.run(debug=True)
