#!/usr/bin/python3

"""
This is the base for the Application
It will run all the classes of the 
application
"""

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def base():
    return ("Hello")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def create_new_account():
    return render_template("createAccount.html")



if __name__ == '__main__':
    app.run(debug=True)
