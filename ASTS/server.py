# Filename: server.py

import ssl
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load server configuration
with open("server-config.json", "r") as server_config_file:
    server_config = json.load(server_config_file)

app.config['SQLALCHEMY_DATABASE_URI'] = server_config['db_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Secure Flask App is running!"

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(server_config['ssl_certfile'], server_config['ssl_keyfile'])
    app.run(ssl_context=context, port=4443)
