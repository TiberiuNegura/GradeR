from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
import uuid

# In caz ca nu va merg comenzile din psycopg2: pip install psycopg2

# Verificati si inlocuiti cu valorile pe care le aveti voi daca sunt diferite, la mine asa erau default
conn = psycopg2.connect(
    host="localhost",
    database="gradeR",
    user="postgres",
    password="1q2w3e"
)


class User:
    def __init__(self, email, password, role, firstName, lastName):
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.firstName = firstName
        self.lastName = lastName
        self.id = str(uuid.uuid4())

    @staticmethod
    def save(user):
        users = User.get_all()
        users[user.id] = user.__dict__
        User._save_to_db(users)

    @staticmethod
    def get_by_username(email):
        users = User.get_all()
        for user in users.values():
            if user['email'] == email:
                return user
        return None

    @staticmethod
    def get_all():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")

        data = cursor.fetchall()

        cursor.close()
        if data:
            return data.__dict__

    @staticmethod
    def _save_to_db(users):
        cursor = conn.cursor()

        try:
            columns = ', '.join(users.keys())
            values = ', '.join(['%s'] * len(users))
            sql = f"INSERT INTO user ({columns}) VALUES ({values})"

            cursor.execute(sql, tuple(users.values()))

            conn.commit()
        except psycopg2.Error as e:
            print(f"Encountered an error: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_student_grades(student_id):

        cursor = conn.cursor()
        query = """
            SELECT 
                g.id_grade, 
                g.value, 
                g.date,
                d.name AS discipline_name
            FROM grade AS g
            JOIN discipline AS d ON g.id_discipline = d.id_discipline
            WHERE g.id_student = %s;
        """
        cursor.execute(query, (student_id,))

        grades = cursor.fetchall()
        cursor.close()
        return grades

    def get_user_id(email):
        cursor = conn.cursor()

        cursor.execute("SELECT id_user FROM user WHERE email = %s", (email))

        result = cursor.fetchone()

        cursor.close()

        return result[0]

    def get_last_name(user_id):
        cursor = conn.cursor()
        
        cursor.execute("SELECT last_name FROM user WHERE id_user = %s", (user_id))

        result = cursor.fetchone()

        cursor.close()

        return result[0]

    def is_teacher(email):
        cursor = conn.cursor()

        cursor.execute("SELECT is_teacher FROM user WHERE email = %s;", (email))

        result = cursor.fetchone()

        cursor.close()

        if result is not None:
            return result[0] 
        else:
            return None 


    def get_student_grades_by_teacher(student_id, teacher_id):
        
        cursor = conn.cursor()
        query = """
            SELECT 
                d.name AS discipline_name, 
                g.value AS grade_value, 
                g.date AS grade_date, 
                t.first_name || ' ' || t.last_name AS teacher_name
            FROM 
                grade g
            JOIN 
                user u ON g.id_student = u.id_user
            JOIN 
                discipline d ON g.id_discipline = d.id_discipline
            JOIN 
                user t ON d.id_teacher = t.id_user
            WHERE 
                g.id_student = %s 
                AND t.is_teacher = true 
                AND t.id_user = %s;
        """

        cursor.execute(query, (student_id,teacher_id))
        
        grades = cursor.fetchall()

        return grades
    
    def get_student_grades_by_discipline(student_id, discipline_id):

        cursor = conn.cursor()
        query = """
            SELECT 
                g.value,
                g.date,
                d.name,
                t.first_name || ' ' || t.last_name AS teacher_name
            FROM grade g
            JOIN discipline d ON g.id_discipline = d.id_discipline
            JOIN user t ON d.id_teacher = t.id_user
            WHERE 
                g.id_student = %s AND 
                t.is_teacher = TRUE AND
                d.id_discipline = %s;
        """

        cursor.execute(query, (student_id, discipline_id))

        grades = cursor.fetchall()

        cursor.close()

        return grades

    def get_all_student_grades(self):
        cursor = conn.cursor()
        query = """
            SELECT 
                g.id_grade, 
                g.value, 
                g.date, 
                g.id_student,
                d.id_discipline, 
                d.name AS discipline_name
            FROM grade g
            JOIN discipline d ON g.id_discipline = d.id_discipline
            WHERE d.id_teacher = %s;
        """
        cursor.execute(query, (self.id,))
        results = cursor.fetchall()
        cursor.close()

        grade_list = []
        for row in results:
            grade_list.append({
                "id_grade": row[0],
                "value": row[1],
                "date": row[2].isoformat() if row[2] else None,
                "student_id": row[3],
                "discipline_id": row[4],
                "discipline": row[5]
            })
        return grade_list

    def get_all_disciplines(self, user_id, is_teacher):
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM discipline")

        data = cursor.fetchall()

        discipline_list = []

        for row in data:
            owns_discipline = False
            if is_teacher:
                owns_discipline = row[1] == user_id
            discipline_list.append({
                "id_discipline": row[0],
                "name": row[2],  
                "teacher": self.get_last_name(row[1]),
                "owns_discipline": owns_discipline 
            })

        cursor.close()

        return discipline_list

    def get_student_grade_by_name(discipline_id, student_id):
        cursor = conn.cursor()

        cursor.execute("SELECT * from grade WHERE id_student = %s AND id_discipline = %s ", (student_id, discipline_id))

        data = cursor.fetchall()

        cursor.close()

        grade_list = []

        for row in data:
            grade_list.append({
                "id": row[0],
                "value": row[3],
                "date": row[4]
            })

        return grade_list

    @staticmethod
    def get_by_id(user_id):
        cursor = conn.cursor()
        cursor.execute('SELECT id_user, email, password, is_teacher FROM "user" WHERE id_user = %s', (user_id,))
        data = cursor.fetchone()
        cursor.close()
        if data:
            return {'id_user': data[0], 'email': data[1], 'password': data[2], 'is_teacher': data[3]}
        return None

    @staticmethod
    def add_grade_record(student_id, discipline_id, value, grade_date=None):
        cursor = conn.cursor()

        if not grade_date:
            grade_date = datetime.utcnow().date()
        sql = ("INSERT INTO grade (id_student, id_discipline, value, date) "
               "VALUES (%s, %s, %s, %s) RETURNING id_grade;")
        cursor.execute(sql, (student_id, discipline_id, value, grade_date))
        new_grade_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return new_grade_id

    def is_assigned_to_discipline(self, discipline_id):
        cursor = conn.cursor()
        cursor.execute("SELECT id_teacher FROM discipline WHERE id_discipline = %s", (discipline_id,))
        discipline_info = cursor.fetchone()
        cursor.close()
        if not discipline_info:
            return False, "Discipline not found"
        if discipline_info[0] != self.id:
            return False, "Teacher is not assigned to this discipline"
        return True, None

    def verify_password(self, password):
        return check_password_hash(self.password, password)
