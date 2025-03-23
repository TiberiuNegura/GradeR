from flask import Blueprint, jsonify

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def home():
    return jsonify({"message": "Welcome to Flask API", "status": "success"}), 200


@web_bp.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200
