from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .__init__ import Base, Session, engine

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    workouts = relationship('Workout', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"