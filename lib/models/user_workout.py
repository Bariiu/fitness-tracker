from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .__init__ import Base, Session, engine

class UserWorkout(Base):
    __tablename__ = 'user_workouts'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)

    completion_date = Column(DateTime, default=func.now())
    notes = Column(String)

    user = relationship("User", back_populates="user_workouts")
    workout = relationship("Workout", back_populates="user_workouts")

    def __repr__(self):
        return (f"<UserWorkout(id={self.id}, user_id={self.user_id}, "
                f"workout_id={self.workout_id}, completion_date={self.completion_date.strftime('%Y-%m-%d') if self.completion_date else 'N/A'})>")

if __name__ == "__main__":
    from .user import User
    from .workout import Workout

    Base.metadata.create_all(engine)
    print("UserWorkout association table created successfully!")

    session = Session()

    user1 = session.query(User).filter_by(name="Alice").first()
    if not user1:
        user1 = User(name="Alice", email="alice@example.com")
        session.add(user1)

    workout1 = session.query(Workout).filter_by(activity="Morning Run").first()
    if not workout1:
        workout1 = Workout(activity="Morning Run", duration_minutes=45)
        session.add(workout1)

    user2 = session.query(User).filter_by(name="Bob").first()
    if not user2:
        user2 = User(name="Bob", email="bob@example.com")
        session.add(user2)

    session.commit()

    assoc1 = UserWorkout(user=user1, workout=workout1, notes="Felt strong!")
    session.add(assoc1)

    assoc2 = UserWorkout(user=user2, workout=workout1, notes="Good group run!")
    session.add(assoc2)

    session.commit()

    print("\nAssociations created:")
    for uw in session.query(UserWorkout).all():
        print(uw)

    print(f"\nWorkouts for Alice:")
    for uw_assoc in user1.user_workouts:
        print(f"- {uw_assoc.workout.activity} on {uw_assoc.completion_date.strftime('%Y-%m-%d')}, Notes: '{uw_assoc.notes}'")

    print(f"\nUsers who did 'Morning Run':")
    for uw_assoc in workout1.user_workouts:
        print(f"- {uw_assoc.user.name} on {uw_assoc.completion_date.strftime('%Y-%m-%d')}, Notes: '{uw_assoc.notes}'")

    session.close()