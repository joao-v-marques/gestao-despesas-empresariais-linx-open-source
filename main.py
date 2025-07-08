import os
from waitress import serve
from dotenv import load_dotenv
from flask import Flask
from configure import config_all

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '')

config_all(app)

if __name__ == "__main__":
    print('Inciando o Servidor Local...')
    serve(app, host='0.0.0.0', port=8080)