#!/usr/bin/python3

"""
This is the code base for VirtualBar.
This module runs most of the program
and operates the important classes and
instructions.
"""

from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'super user'
db = SQLAlchemy(app)

class UserDB(db.Model):
    id = sb.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False )
    userName = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Coilumn(db.Text, unique=True, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login/login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('login/signup.html')


@app.route('/recover', methods=['POST'])
def passwordRecovery():
    return render_templater('login/recover.html')


@app.route('/session', methods=['GET', 'POST'])
def session():
    return render_template('session/session.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile/profile.html')


if __name__ == '__main__':
    app.run(debug=True)
