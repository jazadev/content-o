"""Marks factory"""
from datetime import datetime
from utils import db
from .helpers import random, seed_from_list
from sqlalchemy import select
from models import Inscription, Mark

def add_marks():
    query = select(Inscription.student_id, Inscription.course_id)
    students = db.session.execute(query)
    marks =[] 
    for _ in students:
        mark = {
            "student_id": _.student_id,
            "course_id": _.course_id,
            "mark": random.choice([8.00, 10.00]),
            "date": datetime.strptime("25/07/2024","%d/%m/%Y")
        }
        marks.append(mark)

    seed_from_list(Mark, marks)
    return True