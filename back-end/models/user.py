from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import uuid


#conectezi aici la database lefter in loc de json
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
        self.id = str(uuid.uuid4())

    @staticmethod
    def save(user):
        users = User.get_all()
        users[user.id] = user.__dict__
        User._save_to_file(users)

    @staticmethod
    def get_by_username(email):
        users = User.get_all()
        for user in users.values():
            if user['email'] == email:
                return user
        return None

    @staticmethod
    def get_all():
        if not os.path.exists('users.json'):
            return {}
        with open('users.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def _save_to_file(users):
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
