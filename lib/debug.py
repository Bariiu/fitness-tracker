# lib/debug.py

import ipdb
from datetime import datetime, timedelta

from lib.models.__init__ import engine, Session, Base
from lib.models.user import User
from lib.models.workout import Workout
from lib.models.user_workout import UserWorkout

from lib.helpers import (
    create_user, get_all_users, find_user_by_id, find_user_by_name,
    update_user_email, delete_user,
    create_workout, get_all_workouts, find_workout_by_id,
    update_workout_duration, delete_workout,
    log_user_workout, get_user_workouts, get_workout_participants,
    get_all_workout_logs, delete_user_workout_log
)

from lib.seed import seed_database

def debug_session():
    """
    Starts an interactive debugging session with access to models and helpers.
    """
    print("Welcome to the debug session!")
    print("Available variables:")
    print("  - Session: Your SQLAlchemy session class")
    print("  - User, Workout, UserWorkout: Your database models")
    print("  - All functions from lib/helpers.py (e.g., create_user, get_all_users)")
    print("  - seed_database(): Function to re-seed your database")
    print("  - datetime, timedelta: For date manipulation")
    print("\nTo enter the interactive debugger, type `q` and press Enter.")
    print("To quit this script, type `exit()` or `quit()` in the ipdb/pdb prompt.")

    session = Session()

    ipdb.set_trace()

    session.close()
    print("Debug session ended.")

if __name__ == "__main__":
    debug_session()