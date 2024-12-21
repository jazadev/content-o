"""Students factory"""
from datetime import datetime
from .helpers import seed_from_list, random_date, random
from faker import Faker
from models import Student

fake = Faker("es_MX")

start_date = datetime.strptime("01/01/2010", "%d/%m/%Y")
end_date = datetime.strptime("31/12/2012", "%d/%m/%Y")

def add_students():
    """List of students"""
    students =[] 
    for _ in range(100):
        student = {
            "first_name": fake.first_name()[:50],
            "last_name": f"{fake.last_name()} {fake.last_name()}"[:50],
            "birth_day": random_date(start_date, end_date),
            "address": fake.address().replace("\n", " ")[:120],  # Limit to 120 caracters
            "telephone": f"+52 55 {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
            "email": fake.email()[:50],
            "grade": random.choice(["01", "02", "03"])
        }
        students.append(student)

    seed_from_list(Student, students)
    return True
