"""Seeder database"""
from models import (Student, Teacher, Course, Inscription, Mark, Attendance, 
    Charge, TeacherPayment, CourseExpense)

def seed_tables():
    """Call data seeding factories"""
    from .students_factory import add_students
    add_students()

    from .teachers_factory import add_teachers
    add_teachers()

    from .courses_factory import add_courses
    add_courses()

    from .inscriptions_factory import add_inscriptions
    add_inscriptions()

    from .marks_factory import add_marks
    add_marks()

    from .charges_factory import add_charges
    add_charges()

    from .teachers_payments_factory import add_teachers_payments
    add_teachers_payments()

    from.course_expenses_factory import add_course_expenses
    add_course_expenses()

    return None
