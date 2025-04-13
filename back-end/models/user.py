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
        user_data = {
            'first_name': user.firstName,
            'last_name': user.lastName,
            'email': user.email,
            'password': user.password,  # already hashed
            'is_teacher': user.role
        }
        user.id = User._save_to_db(user_data)

    @staticmethod
    def get_by_username(email):
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()

        if rows:
            return {
                row[0]: dict(zip(columns, row))  # Use row[0] (user_id) as the key
                for row in rows
            }

        return {}

    @staticmethod
    def _save_to_db(user_data):
        cursor = conn.cursor()
        try:
            columns = ', '.join(user_data.keys())
            placeholders = ', '.join(['%s'] * len(user_data))
            sql = 'INSERT INTO users ({}) VALUES ({}) RETURNING id_user;'.format(columns, placeholders)

            cursor.execute(sql, tuple(user_data.values()))
            new_id = cursor.fetchone()[0]
            conn.commit()
            print("User inserted successfully with ID:", new_id)
            return new_id
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Encountered an error: {e}")
        finally:
            cursor.close()

    @staticmethod
    def delete_grade_record(grade_id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grade WHERE id_grade = %s RETURNING id_grade;", (grade_id,))
        deleted = cursor.fetchone()
        conn.commit()
        cursor.close()
        return deleted is not None

    @staticmethod
    def update_grade_record(grade_id, new_value, new_date):
        cursor = conn.cursor()
        sql = "UPDATE grade SET value = %s, date = %s WHERE id_grade = %s RETURNING id_grade;"
        cursor.execute(sql, (new_value, new_date, grade_id))
        updated = cursor.fetchone()
        conn.commit()
        cursor.close()
        return updated is not None

    @staticmethod
    def get_grades_by_student_name(search_term):
        cursor = conn.cursor()

        # Normalize search term to lowercase
        search_term = search_term.lower()

        sql = """
            SELECT g.id_grade, g.value, g.date, d.name AS discipline,
                   u.first_name, u.last_name
            FROM grade g
            JOIN discipline d ON g.id_discipline = d.id_discipline
            JOIN "user" u ON g.id_student = u.id_user
            WHERE LOWER(u.first_name) LIKE %s
               OR LOWER(u.last_name) LIKE %s
               OR LOWER(CONCAT(u.first_name, ' ', u.last_name)) LIKE %s
               OR LOWER(CONCAT(u.last_name, ' ', u.first_name)) LIKE %s;
        """
        like_term = f"%{search_term}%"
        cursor.execute(sql, (like_term, like_term, like_term, like_term))
        results = cursor.fetchall()
        cursor.close()
        return results

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

        cursor.execute("SELECT id_user FROM users WHERE email = %s", (email,))

        result = cursor.fetchone()

        cursor.close()

        return result[0]

    def get_last_name(self, user_id):
        cursor = conn.cursor()

        cursor.execute("SELECT last_name FROM users WHERE id_user = %s", (user_id,))

        result = cursor.fetchone()

        cursor.close()

        return result[0]

    @staticmethod
    def is_teacher(email):
        cursor = conn.cursor()

        cursor.execute("SELECT is_teacher FROM users WHERE email = %s;", (email,))

        result = cursor.fetchone()

        cursor.close()

        if result is not None:
            return result[0]
        else:
            return None

    def get_student_grades_by_teacher(self, student_id, teacher_id):

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
                users u ON g.id_student = u.id_user
            JOIN 
                discipline d ON g.id_discipline = d.id_discipline
            JOIN 
                users t ON d.id_teacher = t.id_user
            WHERE 
                g.id_student = %s 
                AND t.is_teacher = true 
                AND t.id_user = %s;
        """

        cursor.execute(query, (student_id, teacher_id))

        grades = cursor.fetchall()

        return grades

    @staticmethod
    def get_grades_by_discipline_and_teacher(discipline_id, teacher_id):
        cursor = conn.cursor()
        query = """
            SELECT 
                g.id_grade,
                g.value,
                u.first_name || ' ' || u.last_name AS student_name,
                g.date
            FROM grade g
            JOIN users u ON g.id_student = u.id_user
            WHERE g.id_discipline = %s;
        """
        cursor.execute(query, (discipline_id,))
        grades = cursor.fetchall()
        cursor.close()

        grade_list = []
        for row in grades:
            grade_list.append({
                "id": row[0],
                "value": row[1],
                "name": row[2],
                "date": row[3].isoformat() if row[3] else None
            })

        return grade_list

    @staticmethod
    def get_student_grades_by_discipline(discipline_id, student_id):
        cursor = conn.cursor()
        query = """
                    SELECT
                        g.id_grade,
                        g.value,
                        g.date,
                        t.first_name || ' ' || t.last_name AS teacher_name
                    FROM grade g
                    JOIN discipline d ON g.id_discipline = d.id_discipline
                    JOIN users t ON d.id_teacher = t.id_user
                    WHERE 
                        g.id_student = %s AND 
                        t.is_teacher = TRUE AND
                        d.id_discipline = %s;
                """

        cursor.execute(query, (student_id, discipline_id))

        grades = cursor.fetchall()

        grade_list = []
        for row in grades:
            grade_list.append({
                "id": row[0],
                "value": row[1],
                "date": row[2].isoformat() if row[2] else None,
                "name": row[3]
            })

        return grade_list

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
        cursor.execute('SELECT id_user, email, password, is_teacher FROM users WHERE id_user = %s', (user_id,))
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

    @staticmethod
    def is_assigned_to_discipline(discipline_id, teacher_id):
        cursor = conn.cursor()
        cursor.execute("SELECT id_teacher FROM discipline WHERE id_discipline = %s", (discipline_id,))
        discipline_info = cursor.fetchone()
        cursor.close()

        if not discipline_info:
            return False, "Discipline not found"
        if discipline_info[0] != teacher_id:
            return False, "Teacher is not assigned to this discipline"
        return True, None

    @staticmethod
    def get_full_name_by_id(user_id):
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name FROM users WHERE id_user = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return f"{result[0]} {result[1]}"
        return None

    @staticmethod
    def get_user_id_by_full_name(first_name, last_name):
        cursor = conn.cursor()
        cursor.execute("SELECT id_user FROM users WHERE first_name = %s AND last_name = %s", (first_name, last_name))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    @staticmethod
    def update_grade(grade_id, new_value):
        cursor = conn.cursor()
        cursor.execute("UPDATE grade SET value = %s WHERE id_grade = %s", (new_value, grade_id))
        conn.commit()
        cursor.close()

    @staticmethod
    def delete_grade(grade_id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grade WHERE id_grade = %s", (grade_id,))
        conn.commit()
        cursor.close()

    @staticmethod
    def get_all_student_names():
        cursor = conn.cursor()
        query = """
            SELECT first_name, last_name
            FROM users
            WHERE is_teacher = FALSE;
        """
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()

        return [f"{first} {last}" for first, last in students]
    def verify_password(self, password):
        return check_password_hash(self.password, password)
