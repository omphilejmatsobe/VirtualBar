from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(name)

@app.rout('/')
def home():
    return render_template('index.html')
