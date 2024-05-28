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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login/login.html')


@app.route('/signup')
def signup():
    return render_template('login/signup.html')


@app.route('/recover')
def passwordRecovery():
    return render_templater('login/recover.html')


@app.route('/session')
def session():
    return render_template('session/session.html')


@app.route('/profile')
def profile():
    return render_template('profile/profile.html')


if __name__ == '__main__':
    app.run(debug=True)
