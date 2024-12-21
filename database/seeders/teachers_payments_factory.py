"""Teachers Payments factory"""
from .helpers import seed_from_list
from models import TeacherPayment


def add_teachers_payments():
    payments = [
        {
            "teacher_id": 1,
            "course_id": 1,
            "concept": "Impartición de curso",
            "amount": 2000,
        },
        {
            "teacher_id": 6,
            "course_id": 1,
            "concept": "Asistencia en curso",
            "amount": 1000,
        },
        {
            "teacher_id": 2,
            "course_id": 2,
            "concept": "Impartición de curso",
            "amount": 2600,
        },
        {
            "teacher_id": 7,
            "course_id": 2,
            "concept": "Asistencia en curso",
            "amount": 1100,
        },
        {
            "teacher_id": 3,
            "course_id": 3,
            "concept": "Impartición de curso",
            "amount": 3100,
        },
        {
            "teacher_id": 8,
            "course_id": 3,
            "concept": "Asistencia en curso",
            "amount": 1200,
        },
    ]

    seed_from_list(TeacherPayment, payments)
    return True
