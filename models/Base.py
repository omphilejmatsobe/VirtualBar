#!/usr/bin/python3

"""
This is the base for the Application
It will run all the classes of the
application
"""


import flask
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DATABASE = "Users.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{ DATABASE }'
db.init_app(app)


class newUserDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50),  nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)


class userRegistration(FlaskForm):
    """
    Class for the user registration form
    """

    email = EmailField(label='Email', validators=[DataRequired()])
    firstName = StringField(label='First Name', validators=[DataRequired()])
    lastName = StringField(label='Last Name', validators=[DataRequired()])
    userName = StringField(label='Username', validators=[DataRequired(),
                           Length(min=5, max=20)])
    newPasswrd = PasswordField(label='New Password', validators=[DataRequired(),
                           Length(min=5, max=20)])
    confirmPasswrd = PasswordField(label='Confirm Password', validators=[DataRequired(),
                           Length(min=5, max=20)])

    def passwrd_validator(form, field):
        """
        Function that checks for password validation
        """
        if len(newPasswrd) < 8:
            raise ValidationError(_('Password must have at least 8 characters'))

    def confirm_passwrd(form, field):
        """
        function that checks if password is correcti
        """
        if confirmPasswrd != newPasswrd:
            raise ValidationError(_('Passwords do not match'))


class loginPage(FlaskForm):
    """
    Class for user login
    """

    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Enter Password', validators=[DataRequired(), Length(min=5, max=20)])


@app.route("/")
def base():
    return rendirect(url_for('login'))


@app.route("/login", methods=["POST", "GET"])
def login():
    form = loginPage()
    return render_template("login/login.html", form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = userRegistration()
    if request.method == "POST" and form.validate_on_submit():
        user_reg = Register(
                email=form.email.data,
                firstName=form.firstName.data,
                lastName=form.lastName.data,
                userName=form.userName.data,
                password=form.newPasswrd.data
                )

        db.session.add(user_reg)
        db.session.commit()
        flash("Account created succesfully.", category="success")
        return redirect(url_for('login'))

    return render_template("login/signup.html", form=form)


@app.route("/recover")
def recover():
    return render_template("login/recover.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/session")
def session():
    return render_template("session/session.html")


if __name__ == '__main__':
    app.run(debug=True)
