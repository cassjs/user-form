# from flask import Flask, render_template, url_for

# app = Flask(__name__)

# @app.route("/register")
# def register():
#     return render_template('register.html')

# @app.route("/login")
# def login():
#     return render_template('login.html')

# @app.route("/dashboard")
# def dashboard():
#     # Temporary Placeholder
#     return "<p>This is a placeholder. You're looking at the Dashboard.</p>"

# @app.route("/userprofile")
# def userprofile():
#     # Temporary Placeholder
#     return "<p>This is a placeholder. You're looking at your profile.</p>"

import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, session, url_for
from twilio.rest import Client

load_dotenv()
app = Flask(__name__)
# TODO: Need to replace with something else?
app.secret_key = 'secretkeylol'

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE = os.environ.get('TWILIO_VERIFY_SERVICE')
# SENDGRID_API_KEY= os.environ.get('SENDGRID_API_KEY') 

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        to_email = request.form['email']
        session['to_email'] = to_email
        send_verification(to_email)
        return redirect(url_for('generate_verification_code'))
    return render_template('register.html')

# Twilio sends a verification token to the email stored in the current Flask session
def send_verification(to_email):
    verification = client.verify \
        .services(TWILIO_VERIFY_SERVICE) \
        .verifications \
        .create(to=to_email, channel='email')
    print(verification.sid)
    
@app.route('/verifyme', methods=['GET', 'POST'])
def generate_verification_code():
    to_email = session['to_email']
    error = None
    if request.method == 'POST':
        verification_code = request.form['verificationcode']
        if check_verification_token(to_email, verification_code):
            return render_template('success.html', email = to_email)
        else:
            error = "Invalid verification code. Please try again."
            return render_template('verifypage.html', error = error)
    return render_template('verifypage.html', email = to_email)

def check_verification_token(phone, token):
    check = client.verify \
        .services(TWILIO_VERIFY_SERVICE) \
        .verification_checks \
        .create(to=phone, code=token)    
    return check.status == 'approved'
