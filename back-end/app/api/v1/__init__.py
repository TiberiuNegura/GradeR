from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .v1 import bp as v1_bp

api_bp.register_blueprint(v1_bp)