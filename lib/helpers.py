from sqlalchemy.orm import sessionmaker, joinedload
from lib.models.__init__ import engine, Session
from lib.models.user import User
from lib.models.workout import Workout
from lib.models.user_workout import UserWorkout
from datetime import datetime, timedelta
import random

def create_user(name, email):
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
    session = Session()
    try:
        users = session.query(User).all()
        return users
    finally:
        session.close()

def find_user_by_id(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        return user
    finally:
        session.close()

def find_user_by_name(name):
    session = Session()
    try:
        users = session.query(User).filter(User.name.ilike(f'%{name}%')).all()
        return users
    finally:
        session.close()

def update_user_email(user_id, new_email):
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
    session = Session()
    try:
        workouts = session.query(Workout).all()
        return workouts
    finally:
        session.close()

def find_workout_by_id(workout_id):
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        return workout
    finally:
        session.close()

def update_workout_duration(workout_id, new_duration):
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
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            logs = session.query(UserWorkout).options(
                joinedload(UserWorkout.workout),
                joinedload(UserWorkout.user)
            ).filter(UserWorkout.user_id == user_id).all()
            return logs
        return []
    finally:
        session.close()

def get_workout_participants(workout_id):
    session = Session()
    try:
        workout = session.query(Workout).options(
            joinedload(Workout.user_workouts).joinedload(UserWorkout.user)
        ).filter_by(id=workout_id).first()
        if workout:
            return workout.users
        return []
    finally:
        session.close()

def get_all_workout_logs():
    session = Session()
    try:
        logs = session.query(UserWorkout).options(
            joinedload(UserWorkout.user),
            joinedload(UserWorkout.workout)
        ).order_by(UserWorkout.completion_date.desc()).all()
        return logs
    finally:
        session.close()

def delete_user_workout_log(log_id):
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
    from lib.seed import seed_database
    seed_database()
    print("--- Database re-seeded for testing ---")

    print("\n--- Test sequence begins ---")

    initial_users = get_all_users()
    initial_workouts = get_all_workouts()

    if not initial_users or not initial_workouts:
        print("Database is empty even after seeding. Exiting helper test.")
        exit()
    else:
        print(f"\nFound {len(initial_users)} users and {len(initial_workouts)} workouts from seed.")

    print("\n--- Test: Creating User ---")
    unique_email_create = f"test.user.{datetime.now().strftime('%Y%m%d%H%M%S%f')}@gmail.com"
    new_user_created = create_user("Test User", unique_email_create)
    if new_user_created:
        print(f"New user created: {new_user_created}")

    print("\n--- Test: Get All Users (fresh fetch) ---")
    users_after_create = get_all_users()
    for user in users_after_create:
        print(user)

    if users_after_create:
        first_user_id = users_after_create[0].id
        found_user = find_user_by_id(first_user_id)
        print(f"\n--- Test: Find User by ID ({first_user_id}) ---")
        print(f"Found: {found_user}")

    print("\n--- Test: Find User by Name ('Alice') ---")
    alice_users_found = find_user_by_name("Alice")
    print(f"Found: {alice_users_found}")

    if alice_users_found:
        print("\n--- Test: Update User Email ---")
        updated_unique_email = f"alice.updated.{datetime.now().strftime('%Y%m%d%H%M%S%f')}@gmail.com"
        updated_alice = update_user_email(alice_users_found[0].id, updated_unique_email)
        print(f"Updated Alice: {updated_alice}")

    print("\n--- Test: Creating Workout ---")
    new_workout_created = create_workout("Evening Walk", 30)
    if new_workout_created:
        print(f"New workout created: {new_workout_created}")

    print("\n--- Test: Get All Workouts (fresh fetch) ---")
    workouts_after_create = get_all_workouts()
    for workout in workouts_after_create:
        print(workout)

    print("\n--- Test: Logging User Workout ---")
    user_to_log = find_user_by_id(initial_users[0].id)
    workout_to_log_1 = find_workout_by_id(initial_workouts[0].id)
    workout_to_log_2 = find_workout_by_id(initial_workouts[1].id)

    if user_to_log and workout_to_log_1 and workout_to_log_2:
        log_user_workout(user_to_log.id, workout_to_log_1.id, notes="Great energy today!")
        log_user_workout(user_to_log.id, workout_to_log_2.id, completion_date=datetime.now() - timedelta(days=1))
        log_user_workout(user_to_log.id, workout_to_log_1.id, notes="Another attempt, shouldn't add new log.")
    else:
        print("Not enough users/workouts to test logging after re-fetching.")

    user_for_logs_display = find_user_by_id(user_to_log.id)
    print(f"\n--- Test: Get Workouts for {user_for_logs_display.name} (ID: {user_for_logs_display.id}) ---")
    if user_for_logs_display:
        users_workouts_list = get_user_workouts(user_for_logs_display.id)
        if users_workouts_list:
            for uw_log in users_workouts_list:
                print(f"- {uw_log.workout.activity} on {uw_log.completion_date.strftime('%Y-%m-%d %H:%M')}, Notes: {uw_log.notes or 'N/A'}")
        else:
            print(f"No workout logs found for {user_for_logs_display.name}.")
    else:
        print(f"User with ID {user_to_log.id} not found for log display.")

    workout_for_participants_display = find_workout_by_id(initial_workouts[0].id)
    if workout_for_participants_display:
        print(f"\n--- Test: Get Participants for '{workout_for_participants_display.activity}' (ID: {workout_for_participants_display.id}) ---")
        participants = get_workout_participants(workout_for_participants_display.id)
        if participants:
            print(f"Participants: {[p.name for p in participants]}")
        else:
            print("No participants for this workout.")
    else:
        print(f"Workout with ID {initial_workouts[0].id} not found for participants display.")

    print("\n--- Test: Get All Workout Logs ---")
    all_logs_display = get_all_workout_logs()
    for log_entry in all_logs_display[:5]:
        print(f"Log ID: {log_entry.id}, User: {log_entry.user.name}, Workout: {log_entry.workout.activity}, Date: {log_entry.completion_date.strftime('%Y-%m-%d')}")

    users_to_delete_from = get_all_users()
    if users_to_delete_from and len(users_to_delete_from) > 1:
        user_to_delete_target = None
        for u in users_to_delete_from:
            if u.name not in ["Alice", "Test User"]:
                 user_to_delete_target = u
                 break
        if user_to_delete_target:
            print(f"\n--- Test: Deleting User {user_to_delete_target.name} (ID: {user_to_delete_target.id}) ---")
            delete_user(user_to_delete_target.id)
            print("\nUsers remaining:")
            for user in get_all_users():
                print(user)
        else:
            print("\nSkipping delete user test: Not enough diverse users to safely delete without affecting other tests.")

    if new_workout_created:
        print(f"\n--- Test: Deleting Workout '{new_workout_created.activity}' (ID: {new_workout_created.id}) ---")
        delete_workout(new_workout_created.id)
        print("\nWorkouts remaining:")
        for workout in get_all_workouts():
            print(workout)

    all_logs_after_deletions = get_all_workout_logs()
    if all_logs_after_deletions:
        log_to_delete_id = all_logs_after_deletions[0].id
        print(f"\n--- Test: Deleting specific workout log ID: {log_to_delete_id} ---")
        delete_user_workout_log(log_to_delete_id)

        deleted_log_check = next((log for log in get_all_workout_logs() if log.id == log_to_delete_id), None)
        if not deleted_log_check:
            print(f"Log {log_to_delete_id} successfully deleted.")
    else:
        print("\nNo logs to delete for specific log test.")

    print("\n--- Final Data State ---")
    print("\nUsers:")
    for user in get_all_users():
        print(user)
    print("\nWorkouts:")
    for workout in get_all_workouts():
        print(workout)
    print("\nWorkout Logs:")
    for log_entry in get_all_workout_logs():
        print(log_entry)

    print("\n--- Helper function tests complete! ---")