# **user-form**

This is a simple user sign-up and login application. After the user registers, the user will be prompted for a 4-digit verification code sent via the email that was provided by the user at sign up. The [Twilio Verify API](https://www.twilio.com/verify) is used to authenticate the user's email and the email is generated via the [SendGrid Email API](https://sendgrid.com/). To learn how to integrate the two API's, I utilized a Twilio blog post ["How to Verify an Email Address Using Python, Flask, and Twilio Verify"](https://www.twilio.com/blog/verify-email-address-python-flask-twilio-verify) by Diane Phan, then I added some extra functionality of my own.

## **Build**
- **Language & Framework:** Python, Flask
- **Database:** Flask-SQLAlchemy
- **Styling:** Bootstrap, LESS
- **Scripting:** Bash
- **Deployment:** 

## **Features**
- User Sign-in/Sign-up/Logout functionality
- Email Verification code provided after registration
- User data stored via the Flask-SQLAlchemy database
- Security handled via flask login manager and user passwords hashed
- Responsive styling viewable on mobile or desktop devices

## **Preview:**
<img src="static/userform-demo1.png" width="880px" target="_blank">\
<img src="static/userform-demo2.png" width="880px" target="_blank">

## **Getting Started**

### **Clone repository**

    $ git clone https://github.com/cassjs/user-form.git

* Navigate to the project folder

      $ cd user-form
      
### **Docker**

* **Download Docker Desktop:** https://www.docker.com/get-started. There are versions available for Linux, Max, and Windows. **What is Docker?** Docker is a platform for building, running, and shipping applications. Docker packages up an application with everything it needs and allows an app to run and function the same way on any user's local machine.

* **Create a Docker ID:** https://hub.docker.com/signup

* **Login:** You will be prompted to enter your Docker credentials.
      
      $ docker login
      
* **Build Docker Image:** 
      
      $ ./scripts/build.sh
      
* **Run Application/Docker Container:**
      
      $ ./scripts/run.sh
      # Opens a browser http://localhost:5000

### **Editing Application**
* **Stop Running Container:** 

      $ ./scripts/stop.sh  
      
* **Multiple Edits:** For efficiency with multiple edits, it is recommened to create your own virtual enviorment within your local machine. Once all edits are confirmed, just rebuild and run the container with the commands from the Docker section. 

	<details>
		<summary>Click to expand! Create a local virtual enviornment</summary>

	* Create a new virtual environment

	      #conda
	      $ conda create -n myenv python=3.8

		or

	      #venv
	      $ python -m venv myenv

	### **Activate virtual environment**

	* Activate your new virtual environment

	      #conda
	      $ conda activate myenv

		or

	      #venv (Windows)
	      $ myenv/Scripts/activate    

		or

	      #venv (Mac / Unix / WSL)
	      $ source myenv/bin/activate

	### **Install requirements.txt**

	* Install the required packages

	      $ pip install -r requirements.txt

	### **FLASK_ENV Variable**

	* Set the flask environment

	      #Windows
	      $ set FLASK_ENV=app.py

		or

	      #Mac / Unix / WSL
	      $ export FLASK_ENV=app.py


	### **Run application**

	* Run the app using Flask

	      $ flask run

	</details>

## **License**

[MIT License](https://opensource.org/licenses/MIT)\
Copyright (c) 2021 Jessica Cassidy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
