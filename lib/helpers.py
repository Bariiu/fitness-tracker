from sqlalchemy.orm import sessionmaker
from lib.models.__init__ import engine, Session
from lib.models.user import User
from lib.models.workout import Workout
from lib.models.user_workout import UserWorkout
from datetime import datetime, timedelta
import random


def create_user(name, email):
    """Creates and adds a new user to the database."""
    session = Session()
    try:
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        print(f"User created: {new_user}")
        return new_user
    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
        return None
    finally:
        session.close()

def get_all_users():
    """Retrieves all users from the database."""
    session = Session()
    try:
        users = session.query(User).all()
        return users
    finally:
        session.close()

def find_user_by_id(user_id):
    """Finds a user by their ID."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        return user
    finally:
        session.close()

def find_user_by_name(name):
    """Finds users by name (case-insensitive, partial match)."""
    session = Session()
    try:
        users = session.query(User).filter(User.name.ilike(f'%{name}%')).all()
        return users
    finally:
        session.close()

def update_user_email(user_id, new_email):
    """Updates a user's email by ID."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.email = new_email
            session.commit()
            print(f"User {user.name} email updated to {new_email}")
            return user
        print(f"User with ID {user_id} not found.")
        return None
    except Exception as e:
        session.rollback()
        print(f"Error updating user email: {e}")
        return None
    finally:
        session.close()

def delete_user(user_id):
    """Deletes a user and all their associated workouts from the database."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"User {user.name} (ID: {user_id}) and associated workouts deleted.")
            return True
        print(f"User with ID {user_id} not found.")
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting user: {e}")
        return False
    finally:
        session.close()

def create_workout(activity, duration_minutes):
    """Creates and adds a new workout type to the database."""
    session = Session()
    try:
        new_workout = Workout(activity=activity, duration_minutes=duration_minutes)
        session.add(new_workout)
        session.commit()
        print(f"Workout created: {new_workout}")
        return new_workout
    except Exception as e:
        session.rollback()
        print(f"Error creating workout: {e}")
        return None
    finally:
        session.close()

def get_all_workouts():
    """Retrieves all distinct workout types from the database."""
    session = Session()
    try:
        workouts = session.query(Workout).all()
        return workouts
    finally:
        session.close()

def find_workout_by_id(workout_id):
    """Finds a workout type by its ID."""
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        return workout
    finally:
        session.close()

def update_workout_duration(workout_id, new_duration):
    """Updates a workout type's default duration by ID."""
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        if workout:
            workout.duration_minutes = new_duration
            session.commit()
            print(f"Workout '{workout.activity}' duration updated to {new_duration} minutes.")
            return workout
        print(f"Workout with ID {workout_id} not found.")
        return None
    except Exception as e:
        session.rollback()
        print(f"Error updating workout duration: {e}")
        return None
    finally:
        session.close()

def delete_workout(workout_id):
    """Deletes a workout type and all its associations from the database."""
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        if workout:
            session.delete(workout)
            session.commit()
            print(f"Workout '{workout.activity}' (ID: {workout_id}) and its associations deleted.")
            return True
        print(f"Workout with ID {workout_id} not found.")
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting workout: {e}")
        return False
    finally:
        session.close()