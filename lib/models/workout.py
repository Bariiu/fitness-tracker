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

