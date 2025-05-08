from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace these values with your actual database credentials if needed
URL_DATABASE = 'postgresql://postgres:123123123@localhost:5432/quizapp'

# Create the SQLAlchemy engine
engine = create_engine(URL_DATABASE, echo=False)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
