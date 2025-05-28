from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

from lib.models.__init__ import engine, Session, Base
from lib.models.user import User
from lib.models.workout import Workout
from lib.models.user_workout import UserWorkout

def seed_database():
    """
    Populates the database with sample users, workouts, and associations.
    """
    Base.metadata.create_all(engine)

    session = Session()

    print("Seeding database...")

    session.query(UserWorkout).delete()
    session.query(Workout).delete()
    session.query(User).delete()
    session.commit()
    print("Existing data cleared.")

    users_data = [
        {"name": "Alice", "email": "alice@gmail.com"},
        {"name": "Bob", "email": "bob@gmail.com"},
        {"name": "Charlie", "email": "charlie@gmail.com"},
        {"name": "Diana", "email": "diana@gmail.com"},
        {"name": "Eve", "email": "eve@gmail.com"},
    ]
    users = [User(**data) for data in users_data]
    session.add_all(users)
    session.commit()
    print(f"Added {len(users)} users.")

    workouts_data = [
        {"activity": "Morning Run", "duration_minutes": 30},
        {"activity": "Weightlifting (Upper)", "duration_minutes": 60},
        {"activity": "Yoga Flow", "duration_minutes": 45},
        {"activity": "Cycling (Outdoor)", "duration_minutes": 90},
        {"activity": "HIIT Training", "duration_minutes": 25},
        {"activity": "Swimming Laps", "duration_minutes": 40},
        {"activity": "Weightlifting (Lower)", "duration_minutes": 75},
        {"activity": "Meditation", "duration_minutes": 15},
    ]
