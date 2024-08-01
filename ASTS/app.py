from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import ssl
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# Initialize database
db.create_all()

# Authentication endpoint
@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    else:
        return 'Invalid credentials', 403

# API endpoint
@app.route('/api/endpoint', methods=['POST'])
@jwt_required()
def api_endpoint():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Anti-detection endpoint
@app.route('/anti-detection', methods=['POST'])
@jwt_required()
def anti_detection():
    return 'Anti-detection response', 200

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain('certs/server.crt', 'certs/server.key')
    app.run(ssl_context=context, port=4443)
