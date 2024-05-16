#!/usr/bin/python3

"""
This is the base for the Application
It will run all the classes of the 
application
"""

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validator import DataRequired

app = Flask(__name__)

class userRegistration(FlaskForm):
    """
    Class for the user registration form
    """

    email = EmailField(label='Email', validators=[DataRequired()])
    firstName = StringField(label='First Name', validators=[DataRequired()])
    Surname = StringField(label='Last Name', validators=[DataRequired()])
    Username = StringField(label='Username', validators=[DataRequired(), Length(min=5, max=20)])
    newPasswrd = PasswordField(label='New Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirmPasswrd = PasswordField(label='First Name', validators=[DataRequired(), Length(min=5, max=20)])

    def passwrd_validator(form, field):
        """
        Function that checks for password validation
        """

        if len(newPasswrd) < 8:
            raise ValidationError(_('Password must have at least 8 characters'))

    def confirm_passwrd(form, field):
        """
        function that checks if password is correct
        """

        if confirmPasswrd != newPasswrd:
            raise ValidationError(_('Passwords do not match'))



@app.route("/")
def base():
    return ("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

"""
@app.route("/signup")
def create_new_account():
   return render_template("createAccount.html")
"""

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/main")
def main():
    return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True)
