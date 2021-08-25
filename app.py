import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, session, url_for
from twilio.rest import Client

app = Flask(__name__)

# Load enviornment variables
load_dotenv()

# Private keys hidden locally only via .env file
SECRET_KEY = os.environ.get('SECRET_KEY')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE = os.environ.get('TWILIO_VERIFY_SERVICE')
SENDGRID_API_KEY= os.environ.get('SENDGRID_API_KEY') 

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/register', methods=['GET', 'POST'])
# User will provide email at registration and a verification code will be generated via email
def register():
    if request.method == 'POST':
        to_email = request.form['email']
        session['to_email'] = to_email
        send_verification(to_email)
        return redirect(url_for('generate_verification_code'))
    return render_template('register.html')

# Twilio client sends verification code to the user's email
def send_verification(to_email):
    verification = client.verify \
        .services(TWILIO_VERIFY_SERVICE) \
        .verifications \
        .create(to=to_email, channel='email')
    print(verification.sid)
        
@app.route('/verificationcode', methods=['GET', 'POST'])
# The verify page is rendered. 
# If verification code is correct, a success message is returned
# Else, if verification code is invalid, try again error will appear
def generate_verification_code():
    to_email = session['to_email']
    error = None
    if request.method == 'POST':
        verification_code = request.form['verificationcode']
        if check_verification_token(to_email, verification_code):
            return render_template('verifysuccess.html', email = to_email)
        else:
            error = "Invalid verification code. Please try again."
            return render_template('verifycode.html', error = error)
    return render_template('verifycode.html', email = to_email)

# Takes email and the verification code entered by user, then calls the Verify API to check code provided back by user
def check_verification_token(phone, token):
    check = client.verify \
        .services(TWILIO_VERIFY_SERVICE) \
        .verification_checks \
        .create(to=phone, code=token)    
    return check.status == 'approved'

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/userprofile')
def userprofile():
    return render_template('userprofile.html')