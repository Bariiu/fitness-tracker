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

def log_user_workout(user_id, workout_id, completion_date=None, notes=None):
    """
    Logs a specific workout for a user by creating a UserWorkout association.
    'completion_date' defaults to now if not provided.
    """
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        workout = session.query(Workout).filter_by(id=workout_id).first()

        if not user:
            print(f"User with ID {user_id} not found.")
            return None
        if not workout:
            print(f"Workout with ID {workout_id} not found.")
            return None

        date_to_use = completion_date if completion_date else datetime.now()

        existing_log = session.query(UserWorkout).filter(
            UserWorkout.user_id == user_id,
            UserWorkout.workout_id == workout_id,
            UserWorkout.completion_date >= date_to_use.replace(hour=0, minute=0, second=0, microsecond=0),
            UserWorkout.completion_date < date_to_use.replace(hour=23, minute=59, second=59, microsecond=999999)
        ).first()

        if existing_log:
            print(f"User {user.name} already logged '{workout.activity}' on {date_to_use.strftime('%Y-%m-%d')}.")
            return existing_log

        new_user_workout = UserWorkout(
            user=user,
            workout=workout,
            completion_date=date_to_use,
            notes=notes
        )
        session.add(new_user_workout)
        session.commit()
        print(f"Logged workout: User '{user.name}' did '{workout.activity}' on {date_to_use.strftime('%Y-%m-%d')}.")
        return new_user_workout
    except Exception as e:
        session.rollback()
        print(f"Error logging user workout: {e}")
        return None
    finally:
        session.close()

def get_user_workouts(user_id):
    """Retrieves all workout logs for a specific user."""
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            return user.user_workouts
        return []
    finally:
        session.close()

def get_workout_participants(workout_id):
    """Retrieves all users who participated in a specific workout type."""
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        if workout:
            return workout.users
        return []
    finally:
        session.close()

def get_all_workout_logs():
    """Retrieves all user-workout association logs."""
    session = Session()
    try:
        logs = session.query(UserWorkout).order_by(UserWorkout.completion_date.desc()).all()
        return logs
    finally:
        session.close()

def delete_user_workout_log(log_id):
    """Deletes a specific user-workout log entry by its ID."""
    session = Session()
    try:
        log_entry = session.query(UserWorkout).filter_by(id=log_id).first()
        if log_entry:
            session.delete(log_entry)
            session.commit()
            print(f"Workout log (ID: {log_id}) deleted.")
            return True
        print(f"Workout log with ID {log_id} not found.")
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting workout log: {e}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("--- Testing Helper Functions ---")
    session = Session()

    all_users = get_all_users()
    all_workouts = get_all_workouts()

    if not all_users or not all_workouts:
        print("Database is empty. Please run 'python -m lib.seed' first.")
    else:
        print(f"\nFound {len(all_users)} users and {len(all_workouts)} workouts from seed.")

    new_user_example = create_user("Test User", "test@example.com")
    new_workout_example = create_workout("Meditation", 20)

    if all_users and all_workouts:
        log_user_workout(all_users[0].id, all_workouts[0].id, notes="Feeling good!")
        log_user_workout(all_users[1].id, all_workouts[0].id, notes="Group session!")

    if all_users:
        user_workouts_list = get_user_workouts(all_users[0].id)
        print(f"\nWorkouts for {all_users[0].name}:")
        for uw_log in user_workouts_list:
            print(f"- {uw_log.workout.activity} on {uw_log.completion_date.strftime('%Y-%m-%d %H:%M')}, Notes: {uw_log.notes or 'N/A'}")

    if new_user_example:
        delete_user(new_user_example.id)

    session.close()
    print("\n--- Helper function tests complete! ---")