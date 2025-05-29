import click
from datetime import datetime

from lib.helpers import (
    create_user, get_all_users, find_user_by_id, find_user_by_name,
    update_user_email, delete_user,
    create_workout, get_all_workouts, find_workout_by_id,
    update_workout_duration, delete_workout,
    log_user_workout, get_user_workouts, get_workout_participants,
    get_all_workout_logs, delete_user_workout_log
)
from lib.models.user import User
from lib.models.workout import Workout
from lib.models.user_workout import UserWorkout


@click.group()
def cli():
    """Fitness Tracker CLI application."""
    pass 

def display_user(user):
    """Helper to display user details."""
    if user:
        click.echo(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    else:
        click.echo("User not found.")

def display_workout(workout):
    """Helper to display workout details."""
    if workout:
        click.echo(f"ID: {workout.id}, Activity: {workout.activity}, Duration: {workout.duration_minutes} mins")
    else:
        click.echo("Workout not found.")

def display_workout_log(log_entry):
    """Helper to display a user workout log entry."""
    if log_entry:
        user_name = log_entry.user.name if log_entry.user else "N/A"
        workout_activity = log_entry.workout.activity if log_entry.workout else "N/A"
        completion_date_str = log_entry.completion_date.strftime('%Y-%m-%d %H:%M') if log_entry.completion_date else "N/A"
        click.echo(f"Log ID: {log_entry.id}, User: {user_name}, Workout: {workout_activity}, Date: {completion_date_str}, Notes: {log_entry.notes or 'N/A'}")
    else:
        click.echo("Workout log not found.")
