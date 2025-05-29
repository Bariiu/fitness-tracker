from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.models.__init__ import Base

class UserWorkout(Base):
    __tablename__ = 'user_workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    completion_date = Column(DateTime, default=datetime.now)
    notes = Column(String)

    user = relationship("User", back_populates="user_workouts")
    workout = relationship("Workout", back_populates="user_workouts")

    def __repr__(self):
        user_name = "N/A"
        workout_activity = "N/A"

        if hasattr(self, 'user') and self.user is not None and 'user' in self.__dict__:
            user_name = self.user.name
        
        if hasattr(self, 'workout') and self.workout is not None and 'workout' in self.__dict__:
            workout_activity = self.workout.activity

        return (f"<UserWorkout(id={self.id}, User='{user_name}', Workout='{workout_activity}', "
                f"Date={self.completion_date.strftime('%Y-%m-%d %H:%M')}, Notes='{self.notes or 'N/A'}')>")