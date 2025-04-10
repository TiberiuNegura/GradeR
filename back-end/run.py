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
    role = data.get('role')
    firstName = data.get('firstName')
    lastName = data.get('lastName')


    if not email or not password:
        return build_response('Username and password required', 400)

    if User.get_by_username(email):
        return build_response('Username already exists', 409)

    new_user = User(email=email, password=password, role=role, firstName=firstName, lastName=lastName)
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


@app.route('/api/grades', methods=['POST'])
def get_grades():
    data = request.get_json()
    user_id = data.get('id')

    if not user_id:
        return build_response('User id and password required', 400)

    grades = User.get_student_grades(user_id)
    grade_list = []
    for grade in grades:
        grade_dict = {
            "id_grade": grade[0],
            "value": grade[1],
            "date": grade[2].isoformat() if grade[2] else None,
            "discipline": grade[3]
        }
        grade_list.append(grade_dict)

    grade_list_str = json.dumps(grade_list)

    return build_response(grade_list_str, 200)

@app.route('/api/grades/by-teacher', methods=['POST'])
def filter_grades_by_teacher():
    data = request.get_json()
    user_id = data.get('id')
    teacher_id = data.get('teacher_id')

    if not user_id or not teacher_id:
        return build_response('User id and teacher required', 400)

    grades = User.get_student_grades_by_teacher(user_id, teacher_id)

    grade_list = []
    for grade in grades:
        grade_dict = {
            "discipline": grade[0],
            "value": grade[1],
            "date": grade[2].isoformat() if grade[2] else None,
            "teacher": grade[3]
        }
        grade_list.append(grade_dict)

    return build_response(json.dumps(grade_list), 200)


@app.route('/api/grades/by-discipline', methods=['POST'])
def filter_grades_by_discipline():
    data = request.get_json()
    user_id = data.get('id')
    discipline_id = data.get('discipline_id')


    if not user_id or not discipline_id:
        return build_response('User id and discipline required', 400)

    grades = User.get_student_grades_by_discipline(user_id, discipline_id)

    grade_list = []
    for grade in grades:
        grade_dict = {
            "discipline": grade[0],
            "value": grade[1],
            "date": grade[2].isoformat() if grade[2] else None,
            "teacher": grade[3]
        }
        grade_list.append(grade_dict)

    return build_response(json.dumps(grade_list), 200)

@app.route('/api/grades/add', methods=['POST'])
def add_grade_endpoint():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    student_id = data.get('student_id')
    discipline_id = data.get('discipline_id')
    value = data.get('value')
    grade_date = data.get('date')

    if not (teacher_id and student_id and discipline_id and value is not None):
        return build_response("Missing required parameters", 400)

    teacher_data = User.get_by_id(teacher_id)

    if not teacher_data:
        return build_response("Invalid teacher credentials", 401)
    if not teacher_data.get("is_teacher"):
        return build_response("User is not a teacher", 403)

    teacher_instance = User(**teacher_data)
    assigned, error_message = teacher_instance.is_assigned_to_discipline(discipline_id)

    if not assigned:
        if error_message == "Discipline not found":
            return build_response(error_message, 404)
        else:
            return build_response(error_message, 403)

    try:
        User.add_grade_record(student_id, discipline_id, value, grade_date)
    except Exception as e:
        return build_response(f"Error adding grade: {e}", 500)

    return build_response("Grade added successfully", 201)


@app.route('/api/grades/teacher', methods=['POST'])
def view_student_grades():
    data = request.get_json()
    teacher_id = data.get('teacher_id')

    if not teacher_id:
        return build_response("Teacher credentials required", 400)

    teacher_data = User.get_by_id(teacher_id)

    if not teacher_data:
        return build_response("Invalid teacher credentials", 401)
    if not teacher_data.get("is_teacher"):
        return build_response("User is not a teacher", 403)

    teacher_instance = User(**teacher_data)
    grade_list = teacher_instance.get_all_student_grades()

    grade_list_str = json.dumps(grade_list)

    return build_response(grade_list_str, 200)


if __name__ == '__main__':
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)

    app.run(host='0.0.0.0', port=5000, debug=True)
