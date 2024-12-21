"""Seeder helper"""
import random
from datetime import datetime, timedelta
from sqlalchemy import insert
from utils import db


def seed_from_list(cls: object, values: list | None = None) -> None:
    """ Data seeding from list """
    if values is None:
        print(f"The {cls.__tablename__} seeder requires a list of elements.")
        return 1
    if len(values) < 1:
        print(f"The {cls.__tablename__} seeder requires at least one element.")
        return 1

    print(f"* Processing data for {cls.__tablename__} table.")
    db.session.execute(insert(cls).values(values))
    db.session.commit()
    print(f"  {len(values)} rows inserted in {cls.__tablename__} table.")

    return

def random_date(start_date, end_date) -> datetime:
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)
