from sqlalchemy import Column, Integer, ForeignKey, DateTime
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
