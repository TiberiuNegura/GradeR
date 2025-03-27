import os

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)