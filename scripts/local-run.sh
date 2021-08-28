#!/bin/bash

# Open browser
open http://localhost:5000

# Set file and run application
export FLASK_ENV=app.py
flask run