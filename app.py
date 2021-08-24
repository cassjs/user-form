from flask import Flask, render_template, url_for

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
    return "<p>This is a placeholder. You're looking at the Dashboard.</p>"

@app.route("/userprofile")
def userprofile():
    # Temporary Placeholder
    return "<p>This is a placeholder. You're looking at your profile.</p>"
