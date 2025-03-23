from flask import Blueprint, jsonify

bp = Blueprint('v1', __name__, url_prefix='/v1')


@bp.route('/data', methods=['GET'])
def get_data():
    return jsonify({
        "version": "1.0",
        "data": [1, 2, 3, 4, 5]
    })
