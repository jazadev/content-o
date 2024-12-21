"""Course Expenses factory"""
from .helpers import seed_from_list
from models import CourseExpense

def add_course_expenses():
    expenses = [
        {
            "course_id": 1,
            "description": "Materiales y recursos",
            "amount": 500
        },
        {
            "course_id": 1,
            "description": "Marketing",
            "amount": 1000
        },
        {
            "course_id": 2,
            "description": "Materiales y recursos",
            "amount": 675
        },
        {
            "course_id": 2,
            "description": "Marketing",
            "amount": 1000
        },
        {
            "course_id": 1,
            "description": "Materiales y recursos",
            "amount": 500
        },
        {
            "course_id": 1,
            "description": "Marketing",
            "amount": 1250
        },
    ]

    seed_from_list(CourseExpense, expenses)
    return True
