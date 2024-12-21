"""Courses factory"""
from .helpers import seed_from_list
from faker import Faker
from models import Course

fake = Faker("es_MX")

def add_courses():
    """Courses list"""
    courses = [
       {
           "name": "Introducción al Mundo de los Negocios",
           "teacher_id": 1,
           "schedule": "Domingo 06 Julio - Sábado 26 Julio",
           "time_schedule": "9:00 - 13:00",
           "time_frame": 4,
           "time_measure": "hora",
           "modality": "Presencial",
           "class_room": "Aula A",
       },
       {
           "name": "Explorando el Fascinante Mundo de la Medicina",
           "teacher_id": 2,
           "schedule": "Domingo 06 Julio - Sábado 26 Julio",
           "time_schedule": "9:00 - 13:00",
           "time_frame": 4,
           "time_measure": "hora",
           "modality": "Presencial",
           "class_room": "Aula C",
       },
       {
           "name": "Explorando el Mundo de las Tecnologías de la Información",
           "teacher_id": 3,
           "schedule": "Lunes 07 Julio - Viernes 25 Julio",
           "time_schedule": "9:00 - 15:00",
           "time_frame": 6,
           "time_measure": "hora",
           "modality": "En línea",
           "class_room": "Visormeet",
       },
    ]

    seed_from_list(Course, courses)
    return True
