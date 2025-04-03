import json
import os

from flask import Flask, jsonify, Response, request
from flask_cors import CORS

import config
from models.user import User

app: Flask = Flask(__name__)

CORS(app)

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

USERS_FILE = 'users.json'


def build_response(message: str, code: int) -> Response:
    response = jsonify({
        'message': message,
        'code': code
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return build_response('Username and password required', 400)

    if User.get_by_username(email):
        return build_response('Username already exists', 409)

    new_user = User(email=email, password=password)
    User.save(new_user)
    return build_response('User created successfully', 201)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_data = User.get_by_username(email)
    if not user_data or not User(**user_data).verify_password(password):
        return build_response('Invalid credentials', 401)

    return build_response('Login successful', 200)


if __name__ == '__main__':
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)

    app.run(host='0.0.0.0', port=5000, debug=True)
