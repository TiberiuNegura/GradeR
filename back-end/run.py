from flask import Flask, jsonify, Response
from flask_cors import CORS

import config

app: Flask = Flask(__name__)

CORS(app)

app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER


def is_param_valid(json_data: any, property_name: str) -> (bool, float):
    data: any = json_data[property_name]
    if data is not None:
        return True, json_data[property_name]

    return False, 0


def build_response(message: str, code: int) -> Response:
    response = jsonify({
        'message': message,
        'code': code
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


def check_method(desired_method: str, method: str) -> (Response, bool):
    if desired_method != method:
        return build_response('Method not allowed', 500), False

    return build_response('', 200), True


def get_text_from_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


@app.route('/')
def index():
    return "Welcome to the Flask app!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
