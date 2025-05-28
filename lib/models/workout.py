from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .__init__ import Base, Session, engine
from .user import User

class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    activity = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='workouts')

    def __repr__(self):
        return (f"<Workout(id={self.id}, activity='{self.activity}', "
                f"duration_minutes={self.duration_minutes}, user_id={self.user_id})>")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Workout table created successfully!")

    session = Session()

    existing_user = session.query(User).first()
    if not existing_user:
        dummy_user = User(name="Test User", email="test@example.com")
        session.add(dummy_user)
        session.commit()
        existing_user = dummy_user
        print(f"Created dummy user: {existing_user}")

    workouts = session.query(Workout).all()
    print("\nAll workouts:")
    for workout in workouts:
        print(f"{workout} (User: {workout.user.name})")

    session.close()