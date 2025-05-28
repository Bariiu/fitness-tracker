from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from .__init__ import Base, Session, engine
from .user_workout import UserWorkout
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    user_workouts = relationship('UserWorkout', back_populates='user', cascade='all, delete-orphan')

    workouts = association_proxy('user_workouts', 'workout')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

if __name__ == "__main__":
    from .workout import Workout
    Base.metadata.create_all(engine)
    print("User table created successfully!")

    session = Session()

    user_alice = User(name="Alice", email="alice@gmail.com")
    user_bob = User(name="Bob", email="bob@gmail.com")
    session.add_all([user_alice, user_bob])
    session.commit()
    print(f"Added users: {user_alice}, {user_bob}")

    workout_run = Workout(activity="Morning Run", duration_minutes=45)
    workout_yoga = Workout(activity="Yoga Session", duration_minutes=60)
    session.add_all([workout_run, workout_yoga])
    session.commit()
    print(f"Added workouts: {workout_run}, {workout_yoga}")


    user_alice.workouts.append(workout_run)
    user_alice.workouts.append(workout_yoga)
    user_bob.workouts.append(workout_run)

    session.commit()

    print("\nUsers and their workouts:")
    for user in session.query(User).all():
        print(f"{user.name}: {[w.activity for w in user.workouts]}")

    print("\nWorkouts and participants:")
    for workout in session.query(Workout).all():
        print(f"{workout.activity}: {[u.name for u in workout.users]}") # using the 'users' proxy on Workout

    session.close()