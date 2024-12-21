from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Date, ForeignKey, DECIMAL, Enum, Boolean
from sqlalchemy.orm import column_property, relationship
from utils import db

# Tabla de Estudiantes
class Student(db.Model):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = column_property(first_name + " " + last_name)
    birth_day = Column(Date)
    address = Column(String(120))
    telephone = Column(String(20))
    email = Column(String(50))
    grade = Column(String(2))
    
    # inscriptions = relationship("Inscription", back_populates="student")
    # charges = relationship("Charge", back_populates="student")
    # attendances = relationship("Attendance", back_populates="student")
    # marks = relationship("Mark", back_populates="student")

# Tabla de Profesores
class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = column_property(first_name + " " + last_name)
    email = Column(String(50))
    telephone = Column(String(16))
    mayor = Column(String(50))
    
    # courses = relationship("Course", back_populates="teacher")
    # teachers_payments = relationship("TeacherPayment", back_populates="teacher")

# Tabla de Cursos
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    schedule = Column(String(40))
    time_schedule = Column(String(14))
    time_frame = Column(Integer)
    time_measure = Column(String(10))
    modality = Column(String(20))
    class_room = Column(String(20))
    
    # teacher = relationship("Teacher", back_populates="courses")
    # inscriptions = relationship("Inscription", back_populates="course")
    # marks = relationship("Marks", back_populates="course")
    # attendances = relationship("Attendance", back_populates="course")
    # course_expenses = relationship("CourseExpense", back_populates="course")
    # charges = relationship("Charge", back_populates="course")
    # teachers_payments = relationship("TeacherPayment", back_populates="course")

# Tabla de Inscripciones
class Inscription(db.Model):
    __tablename__ = 'inscriptions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'), unique=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    date = Column(Date)
    
    # student = relationship("Student", back_populates="inscriptions")
    # course = relationship("Course", back_populates="inscriptions")

# Tabla de Calificaciones
class Mark(db.Model):
    __tablename__ = 'marks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    mark = Column(DECIMAL(5,2))
    date = Column(Date)
    
    # student = relationship("Student", back_populates="marks")
    # course = relationship("Course", back_populates="marks")

# Tabla de Asistencias
class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    date = Column(Date)
    attendant = Column(Boolean)
    
    # student = relationship("Student", back_populates="attendances")
    # course = relationship("Course", back_populates="attendances")

# Tabla de Cobros
class Charge(db.Model):
    __tablename__ = 'charges'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    charge_type = Column(String(20), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    amount = Column(DECIMAL(10,2), nullable=False)
    charge_date = Column(Date, nullable=False)
    charge_method = Column(String(50))
    
    # student = relationship("Student", back_populates="charges")
    # course = relationship("Course", back_populates="charges")

# Tabla de Pagos a Profesores
class TeacherPayment(db.Model):
    __tablename__ = 'teachers_payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    concept = Column(String(120), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    amount = Column(DECIMAL(10,2), nullable=False)
    
    # teacher = relationship("Teacher", back_populates="teachers_payments")
    # course = relationship("Course", back_populates="teachers_payments")

# Tabla de Gastos por ejecución de Cursos
class CourseExpense(db.Model):
    __tablename__ = 'course_expenses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    description = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    
    # course = relationship("Course", back_populates="course_expenses")
