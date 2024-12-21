"""Charges factory"""
from datetime import datetime
from utils import db
from .helpers import random, seed_from_list, random_date
from sqlalchemy import select
from models import Inscription, Charge

amounts ={
    1: 300,
    2: 400,
    3: 500
}

start_date = datetime.strptime("05/06/2024", "%d/%m/%Y")
end_date = datetime.strptime("04/07/2024", "%d/%m/%Y")

def add_charges():
    query = select(Inscription.student_id, Inscription.course_id)
    students = db.session.execute(query)
    charges =[]

    for _ in students:
        pays = random.randint(1, 2)
        amount = int(amounts[_.course_id]) / int(pays)

        for pay in range(pays):
            charge = {
                "student_id": _.student_id,
                "charge_type": "Curso",
                "course_id": _.course_id,
                "amount": amount,
                "charge_date": random_date(start_date, end_date),
                "charge_method": random.choice(
                        ["Efectivo",
                        "Tarjeta de Crédito",
                        "Tarjeta de Débito",
                        "Transferencia"
                        ]
                    )
            }
            charges.append(charge)

    seed_from_list(Charge, charges)
    return True
