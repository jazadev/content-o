"""Inscriptions factory"""
from datetime import datetime
from utils import db
from .helpers import random, random_date, seed_from_list
from sqlalchemy import select
from models import Student, Inscription

start_date = datetime.strptime("25/05/2024", "%d/%m/%Y")
end_date = datetime.strptime("04/07/2024", "%d/%m/%Y")

def add_inscriptions():
    query = select(Student.id)
    students = list(
            db.session.execute(query).scalars().all()
        )
    students_course_1 = random.sample(students, 24)

    students_2 =[student for student in students if student not in students_course_1]
    students_course_2 = random.sample(students_2, 22)

    students_3 =[student for student in students if student not in students_course_1 and student not in students_course_2]
    students_course_3 = random.sample(students_3, 25)

    # Check if exist repeated
    # set1 = set(students_course_1)
    # set2 = set(students_course_2)
    # set3 = set(students_course_3)
    # repeated = set1.intersection(set2).intersection(set3)
    # print(f"Repeated {list(repeated)}")

    _students = [] 
    for _ in students_course_1:
        _student1 = {
            "student_id": _,
            "course_id": 1,
            "date": random_date(start_date, end_date)
        }
        _students.append(_student1)

    for _ in students_course_2:
        _student2 = {
            "student_id": _,
            "course_id": 2,
            "date": random_date(start_date, end_date)
        }
        _students.append(_student2)
 
    for _ in students_course_3:
        _student3 = {
            "student_id": _,
            "course_id": 3,
            "date": random_date(start_date, end_date)
        }
        _students.append(_student3)

    seed_from_list(Inscription, _students)
    return True
