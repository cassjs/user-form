from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    # Temporary Placeholder
    return "<p>You're looking at the Dashboard.</p>"
