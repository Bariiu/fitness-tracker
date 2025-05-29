from lib.models.__init__ import Session, engine
from lib.models.user import User
from lib.models.workout import Workout
from lib.models.user_workout import UserWorkout
from lib.helpers import (
    create_user, get_all_users, find_user_by_id,
    create_workout, get_all_workouts, find_workout_by_id,
    log_user_workout, get_user_workouts, get_workout_participants,
    get_all_workout_logs, delete_user_workout_log,
    update_user_email, delete_user, update_workout_duration, delete_workout
)
from lib.seed import seed_database
from datetime import datetime
from sqlalchemy.orm import joinedload # Ensure this is imported!

def debug_cli():
    print("--- Re-seeding database for debug session ---")
    seed_database()
    print("--- Database re-seeded ---")

    # It's good practice to get a fresh session here if you're doing
    # ad-hoc queries, even though helpers handle their own sessions.
    session = Session()

    print("\n--- Debugging Session Started ---")
    print("Session object available as 'session'. Models: User, Workout, UserWorkout.")
    print("Helper functions are also imported directly (e.g., create_user, get_all_users).")
    print("Type 'exit()' to quit the debugger.")

    print("\n--- All Users currently in DB ---")
    users = session.query(User).all()
    for user in users:
        print(user)

    print("\n--- All Workouts currently in DB ---")
    workouts = session.query(Workout).all()
    for workout in workouts:
        print(workout)

    print("\n--- Creating a test user via helper ---")
    test_user_email = f"debug_user_{datetime.now().strftime('%H%M%S')}@gmail.com"
    new_test_user = create_user("Debug User", test_user_email)
    if new_test_user:
        print(f"Created: {new_test_user}")
    else:
        print("Failed to create debug user.")

    print("\n--- Logging a workout via helper (Alice - Morning Run) ---")
    # Call the helper, which handles its own session
    logged_workout_result = log_user_workout(1, 1, datetime.now(), "Debugging a workout log!")
    if logged_workout_result:
        # Crucially, re-fetch the object with its relationships eager-loaded
        # in a NEW session so its __repr__ can safely access them for printing.
        fresh_session_for_repr = Session()
        try:
            re_fetched_log_for_print = fresh_session_for_repr.query(UserWorkout).options(
                joinedload(UserWorkout.user),
                joinedload(UserWorkout.workout)
            ).filter_by(id=logged_workout_result.id).first()
            if re_fetched_log_for_print:
                print(f"Logged: {re_fetched_log_for_print}")
            else:
                print(f"Could not re-fetch log ID {logged_workout_result.id} for printing.")
        except Exception as e:
            print(f"Error re-fetching log for printing: {e}")
        finally:
            fresh_session_for_repr.close()
    else:
        print("Failed to log workout.")

    print("\n--- Getting workouts for Alice (ID 1) via helper ---")
    alice_workouts = get_user_workouts(1)
    if alice_workouts:
        for uw_log in alice_workouts:
            print(f"- {uw_log.workout.activity} on {uw_log.completion_date.strftime('%Y-%m-%d %H:%M')}, Notes: {uw_log.notes or 'N/A'}")
    else:
        print("No workouts found for Alice.")

    print("\n--- Getting participants for 'Morning Run' (ID 1) via helper ---")
    morning_run_participants = get_workout_participants(1)
    if morning_run_participants:
        for p in morning_run_participants:
            print(f"- {p.name}")
    else:
        print("No participants found for Morning Run.")

    print("\n--- Direct Session Query Example: Find first user ---")
    first_user = session.query(User).first()
    if first_user:
        print(f"First user by direct query: {first_user.name}")

    # Close the session opened at the beginning of debug_cli
    session.close()
    print("\n--- Debugging Session Finished ---")

if __name__ == "__main__":
    debug_cli()