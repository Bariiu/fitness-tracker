from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///fitness_tracker.db"

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()