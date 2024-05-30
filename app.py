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
    """
    This initializes the database table and columns
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)


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
        user = UserDB.query.filter_by(UserDB.email == email, password=password).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
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

        user = UserDB.query.filter((UserDB.username == username)|(UserDB.email == email)).first()

        if user:
            message = "Account Exists."
        else:
            password = generate_password_hash(password)
            newUser = UserDB(name=name, username=username, email=email, password=password)
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
    return render_templater('login/recover.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    This controls dashboards features
    """

    return render_template('session/dashboard.html', logged_in=True, curr_user=user)


@app.route('/session')
def session():
    """
    This displays the session page
    """

    return render_template('session/session.html')


@app.route('/join')
def join():
    return render_template('session/join.html')


@app.route('/logout')
def logout():
    return redirect( url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    user = UserDB.query.get(session['user_id'])
    if user:
        """
        Do nothing
        """
        usersession = true
    else:
        usersession = false
        return redirect(url_for('login'))

    return render_template('session/profile.html', logged_in=True, curr_user=user)


if __name__ == '__main__':
    app.run(debug=True)
