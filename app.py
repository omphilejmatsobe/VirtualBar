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

        user = UserDB.query.filter((UserDB.name == username)|(UserDB.email == email)).first()

        if user:
            flash("Account already exists", "danger")
        else:
            password = generate_password_hash(password)
            newUser = UserDB(name=name, username=username, email=email, password=password)
            db.session.add(newUser)
            db.session.commit()

            redirect( url_for('login') )

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
            return redirect(url_for('login'))
    return render_templater('login/recover.html')


@app.route('/dashboad', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    user = UserDB.query.get(session['user_id'])
    return render_template('session/dashboard.html', logged_in=True, curr_user=user)


@app.route('/session', methods=['GET', 'POST'])
def session():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    user = UserDB.query.get(session['user_id'])
    return render_template('session/session.html', logged_in=True, curr_user=user)


@app.route('/join')
def join():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    user = UserDB.query.get(session['user_id'])
    return render_template('session/join.html', logged_in=True, curr_user=user)


@app.route('/logout')
def logout():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    session.pop('user_id', none)
    return redirect( url_for(home))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    user = UserDB.query.get(session['user_id'])
    return render_template('session/logout.html', logged_in=True, curr_user=user)


if __name__ == '__main__':
    app.run(debug=True)
