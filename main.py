import os 
from flask import Flask
from dotenv import load_dotenv
from configure import config_all

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '')

config_all(app)

app.run(debug=True)