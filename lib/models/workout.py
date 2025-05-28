from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.associationproxy import association_proxy
from .__init__ import Base, Session, engine
from .user_workout import UserWorkout

if __name__ == "__main__":
    from .user import User

    Base.metadata.create_all(engine)
    print("Workout table created successfully!")

    session = Session()

    user_charlie = User(name="Charlie", email="charlie@gmail.com")
    user_diana = User(name="Diana", email="diana@gmail.com")
    session.add_all([user_charlie, user_diana])
    session.commit()

    workout_weights = Workout(activity="Weightlifting", duration_minutes=90)
    workout_swim = Workout(activity="Swimming", duration_minutes=60)
    session.add_all([workout_weights, workout_swim])
    session.commit()

    workout_weights.users.append(user_charlie)
    workout_weights.users.append(user_diana)
    workout_swim.users.append(user_charlie)

    session.commit()

    print("\nWorkouts and their participants:")
    for workout in session.query(Workout).all():
        print(f"{workout.activity}: {[u.name for u in workout.users]}")

    print("\nUsers and their workouts (fetched via user model):")
    for user in session.query(User).all():
        print(f"{user.name}: {[w.activity for w in user.workouts]}")

    session.close()