#!/usr/bin/python3

"""
This is the base for the Application
It will run all the classes of the
application
"""

from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db.init_app(app)


class registrationDB():
    userId = db.Column(db.integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    firstName = db.Column(db.String(50), unique=True, nullable=True)
    lastName = db.Column(db.String(50), unique=True, nullable=True)
    userName = db.Column(db.String(50), unique=True, nullable=True)
    psswrd = db.Column(db.String(100), unique=True, nullable=True)


class userRegistration(FlaskForm):
    """
    Class for the user registration form
    """

    email = EmailField(label='Email', validators=[DataRequired()])
    firstName = StringField(label='First Name', validators=[DataRequired()])
    Surname = StringField(label='Last Name', validators=[DataRequired()])
    Username = StringField(label='Username', validators=[DataRequired(),
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
    passwrd = PasswordField(label='Enter Password', validators=[DataRequired(), Length(min=5, max=20)])


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
        user = Register(
                email=form.email.data,
                firstName=form.firstName.data,
                surname=form.Surname.data,
                password=form.newPasswrd.data
                )

        db.session.add(user)
        db.session.commit()

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
