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