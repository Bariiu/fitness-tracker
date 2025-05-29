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

@cli.command('add-user')
@click.argument('name')
@click.argument('email')
def add_user_command(name, email):
    """Add a new user."""
    create_user(name, email)

@cli.command('list-users')
def list_users_command():
    """List all users."""
    users = get_all_users()
    if users:
        click.echo("\n--- All Users ---")
        for user in users:
            display_user(user)
    else:
        click.echo("No users found.")

@cli.command('find-user')
@click.option('--id', type=int, help='User ID to find.')
@click.option('--name', help='User name (partial match) to find.')
def find_user_command(id, name):
    """Find a user by ID or name."""
    if id:
        user = find_user_by_id(id)
        display_user(user)
    elif name:
        users = find_user_by_name(name)
        if users:
            click.echo("\n--- Matching Users ---")
            for user in users:
                display_user(user)
        else:
            click.echo(f"No users found matching '{name}'.")
    else:
        click.echo("Please provide either --id or --name.")

@cli.command('update-user-email')
@click.argument('user_id', type=int)
@click.argument('new_email')
def update_user_email_command(user_id, new_email):
    """Update a user's email."""
    update_user_email(user_id, new_email)

@cli.command('delete-user')
@click.argument('user_id', type=int)
def delete_user_command(user_id):
    """Delete a user by ID."""
    delete_user(user_id)


@cli.command('add-workout')
@click.argument('activity')
@click.argument('duration', type=int)
def add_workout_command(activity, duration):
    """Add a new workout type."""
    create_workout(activity, duration)

@cli.command('list-workouts')
def list_workouts_command():
    """List all workout types."""
    workouts = get_all_workouts()
    if workouts:
        click.echo("\n--- All Workout Types ---")
        for workout in workouts:
            display_workout(workout)
    else:
        click.echo("No workout types found.")

@cli.command('find-workout')
@click.argument('workout_id', type=int)
def find_workout_command(workout_id):
    """Find a workout type by ID."""
    workout = find_workout_by_id(workout_id)
    display_workout(workout)

@cli.command('update-workout-duration')
@click.argument('workout_id', type=int)
@click.argument('new_duration', type=int)
def update_workout_duration_command(workout_id, new_duration):
    """Update a workout type's default duration."""
    update_workout_duration(workout_id, new_duration)

@cli.command('delete-workout')
@click.argument('workout_id', type=int)
def delete_workout_command(workout_id):
    """Delete a workout type by ID."""
    delete_workout(workout_id)
