from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from twilio.rest import Client
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load enviornment variables
load_dotenv()

# Twilio Private keys hidden locally only via .env file
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE = os.environ.get('TWILIO_VERIFY_SERVICE')
SENDGRID_API_KEY= os.environ.get('SENDGRID_API_KEY') 

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Welcome username')
                return redirect(url_for('dashboard'))
            else:
                print("Authentication failed. Invalid username or password. Try again.")
                return render_template('login.html')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    if request.method == 'POST':
        to_email = request.form['email']
        session['to_email'] = to_email
        send_verification(to_email)
        return redirect(url_for('generate_verification_code'))
    return render_template('signup.html', form=form)

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
            return redirect(url_for('login'))
        else:
            error = "Invalid verification code. Try again."
            return render_template('verifycode.html', error = error)
    return render_template('verifycode.html', email = to_email)

# Takes email and the verification code entered by user, then calls the Verify API to check code provided back by user
def check_verification_token(phone, token):
    check = client.verify \
        .services(TWILIO_VERIFY_SERVICE) \
        .verification_checks \
        .create(to=phone, code=token)    
    return check.status == 'approved'

if __name__ == '__main__':
    app.run(debug=True)