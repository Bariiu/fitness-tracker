# lib/helpers.py
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
        _ = new_user.id
        _ = new_user.name
        _ = new_user.email
        print(f"User created: {new_user}")
        return new_user
    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
        return None
    finally:
        if session.is_active:
            session.close()

def get_all_users():
    session = Session()
    try:
        users = session.query(User).all()
        for user in users:
            _ = user.id 
        return users
    finally:
        if session.is_active:
            session.close()

def find_user_by_id(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            _ = user.id
        return user
    finally:
        if session.is_active:
            session.close()

def find_user_by_name(name):
    session = Session()
    try:
        users = session.query(User).filter(User.name.ilike(f'%{name}%')).all()
        for user in users:
            _ = user.id
        return users
    finally:
        if session.is_active:
            session.close()

def update_user_email(user_id, new_email):
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.email = new_email
            session.commit()
            _ = user.id
            _ = user.email
            print(f"User {user.name} email updated to {new_email}")
            return user
        print(f"User with ID {user_id} not found.")
        return None
    except Exception as e:
        session.rollback()
        print(f"Error updating user email: {e}")
        return None
    finally:
        if session.is_active:
            session.close()

def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user_name = user.name
            session.delete(user)
            session.commit()
            print(f"User {user_name} (ID: {user_id}) and associated workouts deleted.")
            return True
        print(f"User with ID {user_id} not found.")
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting user: {e}")
        return False
    finally:
        if session.is_active:
            session.close()

def create_workout(activity, duration_minutes):
    session = Session()
    try:
        new_workout = Workout(activity=activity, duration_minutes=duration_minutes)
        session.add(new_workout)
        session.commit()
        _ = new_workout.id
        _ = new_workout.activity
        print(f"Workout created: {new_workout}")
        return new_workout
    except Exception as e:
        session.rollback()
        print(f"Error creating workout: {e}")
        return None
    finally:
        if session.is_active:
            session.close()

def get_all_workouts():
    session = Session()
    try:
        workouts = session.query(Workout).all()
        for workout in workouts:
            _ = workout.id
        return workouts
    finally:
        if session.is_active:
            session.close()

def find_workout_by_id(workout_id):
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        if workout:
            _ = workout.id
        return workout
    finally:
        if session.is_active:
            session.close()

def update_workout_duration(workout_id, new_duration):
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        if workout:
            workout.duration_minutes = new_duration
            session.commit()
            _ = workout.id
            _ = workout.duration_minutes
            print(f"Workout '{workout.activity}' duration updated to {new_duration} minutes.")
            return workout
        print(f"Workout with ID {workout_id} not found.")
        return None
    except Exception as e:
        session.rollback()
        print(f"Error updating workout duration: {e}")
        return None
    finally:
        if session.is_active:
            session.close()

def delete_workout(workout_id):
    session = Session()
    try:
        workout = session.query(Workout).filter_by(id=workout_id).first()
        if workout:
            workout_activity = workout.activity
            session.delete(workout)
            session.commit()
            print(f"Workout '{workout_activity}' (ID: {workout_id}) and its associations deleted.")
            return True
        print(f"Workout with ID {workout_id} not found.")
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting workout: {e}")
        return False
    finally:
        if session.is_active:
            session.close()

def log_user_workout(user_id, workout_id, completion_date=None, notes=None):
    session = Session()
    return_instance = None
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
        
        day_start = date_to_use.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = date_to_use.replace(hour=23, minute=59, second=59, microsecond=999999)

        existing_log = session.query(UserWorkout).filter(
            UserWorkout.user_id == user_id,
            UserWorkout.workout_id == workout_id,
            UserWorkout.completion_date >= day_start,
            UserWorkout.completion_date <= day_end
        ).first()

        if existing_log:
            print(f"User {user.name} already logged '{workout.activity}' on {date_to_use.strftime('%Y-%m-%d')}.")
            _ = existing_log.id
            _ = existing_log.completion_date
            _ = existing_log.notes
            return_instance = existing_log
        else:
            new_log_entry = UserWorkout(
                user=user, 
                workout=workout,
                completion_date=date_to_use,
                notes=notes
            )
            session.add(new_log_entry)
            session.commit()
            _ = new_log_entry.id
            _ = new_log_entry.completion_date
            _ = new_log_entry.notes
            
            print(f"Logged workout: User '{user.name}' did '{workout.activity}' on {date_to_use.strftime('%Y-%m-%d')}.")
            return_instance = new_log_entry
        
        return return_instance
    except Exception as e:
        session.rollback()
        print(f"Error logging user workout: {e}")
        return None
    finally:
        if session.is_active:
            session.close()


def get_user_workouts(user_id):
    session = Session()
    try:
        logs = session.query(UserWorkout).options(
            joinedload(UserWorkout.user),
            joinedload(UserWorkout.workout)
        ).filter(UserWorkout.user_id == user_id).all()
        for log_entry in logs:
            _ = log_entry.id
            _ = log_entry.completion_date
        return logs
    finally:
        if session.is_active:
            session.close()

def get_workout_participants(workout_id):
    session = Session()
    try:
        workout = session.query(Workout).options(
            joinedload(Workout.user_workouts).joinedload(UserWorkout.user)
        ).filter_by(id=workout_id).first()
        
        if workout:
            participants = workout.users
            for p in participants:
                _ = p.id
            return participants
        return []
    finally:
        if session.is_active:
            session.close()

def get_all_workout_logs():
    session = Session()
    try:
        logs = session.query(UserWorkout).options(
            joinedload(UserWorkout.user),
            joinedload(UserWorkout.workout)
        ).order_by(UserWorkout.completion_date.desc()).all()
        for log_entry in logs:
            _ = log_entry.id
            _ = log_entry.completion_date
        return logs
    finally:
        if session.is_active:
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
        if session.is_active:
            session.close()

if __name__ == "__main__":
    from lib.seed import seed_database
    
    print("--- Re-seeding database for helpers.py test sequence ---")
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
    new_user_created = create_user("Test User Helpers", unique_email_create)
    if new_user_created:
        print(f"New user created by helper: {new_user_created}") 
        fetched_new_user = find_user_by_id(new_user_created.id)
        print(f"Re-fetched new user: {fetched_new_user}")


    print("\n--- Test: Get All Users (fresh fetch) ---")
    users_after_create = get_all_users()
    for user_item in users_after_create: 
        print(user_item)

    if users_after_create:
        first_user_id = users_after_create[0].id
        found_user = find_user_by_id(first_user_id)
        print(f"\n--- Test: Find User by ID ({first_user_id}) ---")
        print(f"Found: {found_user}")

    print("\n--- Test: Find User by Name ('Alice') ---")
    alice_users_found = find_user_by_name("Alice")
    if alice_users_found:
        print(f"Found matching 'Alice':")
        for u in alice_users_found: print(u)


    if alice_users_found: 
        print("\n--- Test: Update User Email ---")
        updated_unique_email = f"alice.updated.{datetime.now().strftime('%Y%m%d%H%M%S%f')}@gmail.com"
        updated_alice = update_user_email(alice_users_found[0].id, updated_unique_email)
        print(f"Updated Alice: {updated_alice}")
        refetched_alice = find_user_by_id(alice_users_found[0].id)
        print(f"Re-fetched Alice after email update: {refetched_alice}")


    print("\n--- Test: Creating Workout ---")
    new_workout_created = create_workout("Evening Stroll Test", 35)
    if new_workout_created:
        print(f"New workout created by helper: {new_workout_created}")
        fetched_new_workout = find_workout_by_id(new_workout_created.id)
        print(f"Re-fetched new workout: {fetched_new_workout}")


    print("\n--- Test: Get All Workouts (fresh fetch) ---")
    workouts_after_create = get_all_workouts()
    for workout_item in workouts_after_create: 
        print(workout_item)

    print("\n--- Test: Logging User Workout ---")
    user_to_log_for = initial_users[0] 
    workout_to_log_1 = initial_workouts[0]
    workout_to_log_2 = initial_workouts[1] if len(initial_workouts) > 1 else initial_workouts[0]

    print(f"Logging '{workout_to_log_1.activity}' for '{user_to_log_for.name}'")
    log1_result = log_user_workout(user_to_log_for.id, workout_to_log_1.id, notes="Great energy today in helper test!")
    if log1_result: print(f"Log 1 result: {log1_result}")

    print(f"Logging '{workout_to_log_2.activity}' for '{user_to_log_for.name}' (yesterday)")
    log2_result = log_user_workout(user_to_log_for.id, workout_to_log_2.id, completion_date=datetime.now() - timedelta(days=1))
    if log2_result: print(f"Log 2 result: {log2_result}")

    print(f"Attempting to re-log '{workout_to_log_1.activity}' for '{user_to_log_for.name}' (today, should exist)")
    log1_repeat_result = log_user_workout(user_to_log_for.id, workout_to_log_1.id, notes="Another attempt, should not add new log.")
    if log1_repeat_result: print(f"Log 1 repeat result: {log1_repeat_result}")


    print(f"\n--- Test: Get Workouts for {user_to_log_for.name} (ID: {user_to_log_for.id}) ---")
    users_workouts_list = get_user_workouts(user_to_log_for.id) 
    if users_workouts_list:
        for uw_log in users_workouts_list:
            print(f"- {uw_log.workout.activity} by {uw_log.user.name} on {uw_log.completion_date.strftime('%Y-%m-%d %H:%M')}, Notes: {uw_log.notes or 'N/A'}")
    else:
        print(f"No workout logs found for {user_to_log_for.name}.")


    workout_for_participants_display = initial_workouts[0]
    print(f"\n--- Test: Get Participants for '{workout_for_participants_display.activity}' (ID: {workout_for_participants_display.id}) ---")
    participants = get_workout_participants(workout_for_participants_display.id) 
    if participants:
        print(f"Participants: {[p.name for p in participants]}") 
    else:
        print("No participants for this workout.")


    print("\n--- Test: Get All Workout Logs ---")
    all_logs_display = get_all_workout_logs() 
    for log_entry_item in all_logs_display[:5]: 
        print(f"Log ID: {log_entry_item.id}, User: {log_entry_item.user.name}, Workout: {log_entry_item.workout.activity}, Date: {log_entry_item.completion_date.strftime('%Y-%m-%d')}")


    users_for_deletion_test = get_all_users()
    user_to_delete_target = next((u for u in users_for_deletion_test if u.name not in ["Alice", "Test User Helpers"]), None)

    if user_to_delete_target:
        print(f"\n--- Test: Deleting User {user_to_delete_target.name} (ID: {user_to_delete_target.id}) ---")
        delete_user(user_to_delete_target.id)
        print("\nUsers remaining:")
        for user_item_after_delete in get_all_users(): print(user_item_after_delete)
    else:
        print("\nSkipping delete user test: Could not find a suitable non-critical user to delete.")

    if new_workout_created: 
        refetched_before_delete = find_workout_by_id(new_workout_created.id)
        if refetched_before_delete:
            print(f"\n--- Test: Deleting Workout '{refetched_before_delete.activity}' (ID: {refetched_before_delete.id}) ---")
            delete_workout(refetched_before_delete.id)
            print("\nWorkouts remaining:")
            for workout_item_after_delete in get_all_workouts(): print(workout_item_after_delete)
        else:
            print(f"\nSkipping delete workout test: Workout '{new_workout_created.activity}' (ID: {new_workout_created.id}) no longer exists (possibly deleted in a previous run).")


    all_logs_for_delete_test = get_all_workout_logs()
    if all_logs_for_delete_test:
        log_to_delete_id = all_logs_for_delete_test[0].id
        print(f"\n--- Test: Deleting specific workout log ID: {log_to_delete_id} ---")
        delete_user_workout_log(log_to_delete_id)
        deleted_log_check = next((log_item for log_item in get_all_workout_logs() if log_item.id == log_to_delete_id), None)
        if not deleted_log_check:
            print(f"Log {log_to_delete_id} successfully deleted.")
        else:
            print(f"Log {log_to_delete_id} still found after deletion attempt.")
    else:
        print("\nNo logs to delete for specific log test.")

    print("\n--- Final Data State (End of Helper Tests) ---")
    print("\nUsers:")
    for final_user in get_all_users(): print(final_user)
    print("\nWorkouts:")
    for final_workout in get_all_workouts(): print(final_workout)
    print("\nWorkout Logs (first 5):")
    for final_log_entry in get_all_workout_logs()[:5]: print(final_log_entry)

    print("\n--- Helper function tests complete! ---")

