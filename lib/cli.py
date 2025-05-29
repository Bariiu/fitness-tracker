import sys
from datetime import datetime
from lib.helpers import (
    create_user, get_all_users, find_user_by_id, find_user_by_name,
    update_user_email, delete_user,
    create_workout, get_all_workouts, find_workout_by_id,
    update_workout_duration, delete_workout,
    log_user_workout, get_user_workouts, get_workout_participants,
    get_all_workout_logs, delete_user_workout_log
)

def display_main_menu():
    print("\n--- Fitness Tracker CLI ---")
    print("1. Manage Users")
    print("2. Manage Workouts")
    print("3. Manage Workout Logs")
    print("4. Exit")
    print("--------------------------")

def display_user_menu():
    print("\n--- User Management ---")
    print("1. Add New User")
    print("2. View All Users")
    print("3. Find User by ID")
    print("4. Find User by Name")
    print("5. Update User Email")
    print("6. Delete User")
    print("7. Back to Main Menu")
    print("-------------------------")

def display_workout_menu():
    print("\n--- Workout Management ---")
    print("1. Add New Workout Type")
    print("2. View All Workout Types")
    print("3. Find Workout by ID")
    print("4. Update Workout Duration")
    print("5. Delete Workout Type")
    print("6. Back to Main Menu")
    print("--------------------------")

def display_log_menu():
    print("\n--- Workout Log Management ---")
    print("1. Log a Workout for a User")
    print("2. View All Workout Logs")
    print("3. View Workouts for a Specific User")
    print("4. View Participants for a Specific Workout")
    print("5. Delete a Specific Workout Log")
    print("6. Back to Main Menu")
    print("------------------------------")

def get_user_input(prompt, type_func=str):
    while True:
        try:
            return type_func(input(prompt))
        except ValueError:
            print("Invalid input. Please try again.")

def handle_user_management():
    while True:
        display_user_menu()
        choice = get_user_input("Enter your choice: ", int)

        if choice == 1:
            name = get_user_input("Enter user's name: ")
            email = get_user_input("Enter user's email: ")
            create_user(name, email)
        elif choice == 2:
            users = get_all_users()
            if users:
                print("\n--- All Users ---")
                for user in users:
                    print(user)
            else:
                print("No users found.")
        elif choice == 3:
            user_id = get_user_input("Enter user ID: ", int)
            user = find_user_by_id(user_id)
            if user:
                print(f"\nFound user: {user}")
            else:
                print(f"User with ID {user_id} not found.")
        elif choice == 4:
            name = get_user_input("Enter user name (partial match): ")
            users = find_user_by_name(name)
            if users:
                print(f"\n--- Users matching '{name}' ---")
                for user in users:
                    print(user)
            else:
                print(f"No users found matching '{name}'.")
        elif choice == 5:
            user_id = get_user_input("Enter user ID to update email: ", int)
            new_email = get_user_input("Enter new email: ")
            update_user_email(user_id, new_email)
        elif choice == 6:
            user_id = get_user_input("Enter user ID to delete: ", int)
            if get_user_input("Are you sure you want to delete this user and all their workout logs? (yes/no): ").lower() == 'yes':
                delete_user(user_id)
            else:
                print("User deletion cancelled.")
        elif choice == 7:
            break
        else:
            print("Invalid choice. Please try again.")

def handle_workout_management():
    while True:
        display_workout_menu()
        choice = get_user_input("Enter your choice: ", int)

        if choice == 1:
            activity = get_user_input("Enter workout activity name: ")
            duration = get_user_input("Enter default duration in minutes: ", int)
            create_workout(activity, duration)
        elif choice == 2:
            workouts = get_all_workouts()
            if workouts:
                print("\n--- All Workout Types ---")
                for workout in workouts:
                    print(workout)
            else:
                print("No workout types found.")
        elif choice == 3:
            workout_id = get_user_input("Enter workout ID: ", int)
            workout = find_workout_by_id(workout_id)
            if workout:
                print(f"\nFound workout: {workout}")
            else:
                print(f"Workout with ID {workout_id} not found.")
        elif choice == 4:
            workout_id = get_user_input("Enter workout ID to update duration: ", int)
            new_duration = get_user_input("Enter new duration in minutes: ", int)
            update_workout_duration(workout_id, new_duration)
        elif choice == 5:
            workout_id = get_user_input("Enter workout ID to delete: ", int)
            if get_user_input("Are you sure you want to delete this workout type and all its logs? (yes/no): ").lower() == 'yes':
                delete_workout(workout_id)
            else:
                print("Workout deletion cancelled.")
        elif choice == 6:
            break
        else:
            print("Invalid choice. Please try again.")

def handle_workout_log_management():
    while True:
        display_log_menu()
        choice = get_user_input("Enter your choice: ", int)

        if choice == 1:
            user_id = get_user_input("Enter user ID: ", int)
            workout_id = get_user_input("Enter workout ID: ", int)
            completion_date_str = get_user_input("Enter completion date (YYYY-MM-DD, leave blank for today): ")
            notes = get_user_input("Enter notes (optional, leave blank for N/A): ")

            completion_date = None
            if completion_date_str:
                try:
                    completion_date = datetime.strptime(completion_date_str, '%Y-%m-%d')
                except ValueError:
                    print("Invalid date format. Using today's date.")

            log_user_workout(user_id, workout_id, completion_date, notes if notes else None)
        elif choice == 2:
            all_logs = get_all_workout_logs()
            if all_logs:
                print("\n--- All Workout Logs ---")
                for log_entry in all_logs:
                    print(f"Log ID: {log_entry.id}, User: {log_entry.user.name}, Workout: {log_entry.workout.activity}, Date: {log_entry.completion_date.strftime('%Y-%m-%d %H:%M')}, Notes: {log_entry.notes or 'N/A'}")
            else:
                print("No workout logs found.")
        elif choice == 3:
            user_id = get_user_input("Enter user ID to view workouts: ", int)
            user_workouts = get_user_workouts(user_id)
            if user_workouts:
                print(f"\n--- Workouts for User ID {user_id} ---")
                for uw_log in user_workouts:
                    print(f"- {uw_log.workout.activity} on {uw_log.completion_date.strftime('%Y-%m-%d %H:%M')}, Notes: {uw_log.notes or 'N/A'}")
            else:
                print(f"No workout logs found for user ID {user_id}.")
        elif choice == 4:
            workout_id = get_user_input("Enter workout ID to view participants: ", int)
            participants = get_workout_participants(workout_id)
            if participants:
                print(f"\n--- Participants for Workout ID {workout_id} ---")
                for p in participants:
                    print(f"- {p.name}")
            else:
                print(f"No participants found for workout ID {workout_id}.")
        elif choice == 5:
            log_id = get_user_input("Enter workout log ID to delete: ", int)
            if get_user_input("Are you sure you want to delete this specific workout log? (yes/no): ").lower() == 'yes':
                delete_user_workout_log(log_id)
            else:
                print("Workout log deletion cancelled.")
        elif choice == 6:
            break
        else:
            print("Invalid choice. Please try again.")

def cli():
    while True:
        display_main_menu()
        choice = get_user_input("Enter your choice: ", int)

        if choice == 1:
            handle_user_management()
        elif choice == 2:
            handle_workout_management()
        elif choice == 3:
            handle_workout_log_management()
        elif choice == 4:
            print("Exiting Fitness Tracker. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    cli()