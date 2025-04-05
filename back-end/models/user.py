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
            cursor.close
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

    def verify_password(self, password):
        return check_password_hash(self.password, password)
