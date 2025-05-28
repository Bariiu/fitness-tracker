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
    workouts = [Workout(**data) for data in workouts_data]
    session.add_all(workouts)
    session.commit()
    print(f"Added {len(workouts)} workouts.")

    print("Creating user-workout associations...")
    start_date = datetime.now() - timedelta(days=30)

    for user in users:
        num_workouts = random.randint(2, 6)
        selected_workouts = random.sample(workouts, num_workouts)

        for workout in selected_workouts:
            days_offset = random.randint(0, 29)
            hours_offset = random.randint(0, 23)
            minutes_offset = random.randint(0, 59)
            completion_date = start_date + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)

            notes = None
            if random.random() < 0.3:
                notes_options = [
                    "Felt great!",
                    "A bit tired today.",
                    "Pushed hard!",
                ]
                notes = random.choice(notes_options)

            association = UserWorkout(
                user=user,
                workout=workout,
                completion_date=completion_date,
                notes=notes
            )
            session.add(association)
    session.commit()
    print("User-workout associations created.")

    session.close()
    print("Database seeding complete!")

if __name__ == "__main__":
    seed_database()