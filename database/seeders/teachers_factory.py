"""Tachers factory"""
from datetime import datetime
from .helpers import seed_from_list, random
from faker import Faker
from models import Teacher

fake = Faker("es_MX")

grados_academicos = [
    "Maestría en Historia",
    "Maestría en Español",
    "Maestría en Biología Molecular",
    "Maestría en Filosofía Contemporánea",
    "Maestría en Sociología Aplicada",
    "Maestría en Ciencias Políticas",
    "Maestría en Literatura Comparada",
    "Maestría en Psicología Clínica",
    "Maestría en Antropología Social",
    "Maestría en Educación",
    "Doctorado en Historia del Arte",
    "Doctorado en Filosofía y Letras",
    "Doctorado en Biología Celular",
    "Doctorado en Sociología Crítica",
    "Doctorado en Ciencias Políticas",
    "Doctorado en Psicología del Comportamiento",
    "Doctorado en Antropología Cultural",
    "Doctorado en Educación Inclusiva",
    "Doctorado en Literatura Hispanoamericana",
    "Doctorado en Estudios Interdisciplinarios"
]

def add_teachers():
    """List of teachers"""
    teachers = [
       {
           "first_name": "Alejandro",
           "last_name": "Morales",
           "email": "alex@falso.local.edu.mx",
           "telephone": "+52 55 0102 0304",
           "mayor": "Maestría en Finanzas"
       },
       {
           "first_name": "Laura",
           "last_name": "Rodríguez",
           "email": "laura@umed.local.mx",
           "telephone": "+52 55 0203 0405",
           "mayor": "Doctorado en Ciencias Médicas"
       },
       {
           "first_name": "Carlos",
           "last_name": "Fernández",
           "email": "carlos@unti.local.co",
           "telephone": "+52 55 0304 0506",
           "mayor": "Maestría en Ciencias de la Computación"
       }
    ]

    for _ in range(11):
        teacher = {
            "first_name": fake.first_name()[:50],  # Limitar a 50 caracteres
            "last_name": f"{fake.last_name()} {fake.last_name()}"[:50],  # Limitar a 50 caracteres
            "email": fake.email()[:50],  # Limitar a 50 caracteres
            "telephone": f"+52 55 {random.randint(1000, 9999)} {random.randint(1000, 9999)}"[:16],
            "mayor": random.choice(grados_academicos)[:50]  # Limitar a 50 caracteres
        }
        teachers.append(teacher)

    seed_from_list(Teacher, teachers)
    return True
