from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)

    # Establish relationship with Choices
    choices = relationship("Choices", back_populates="question", cascade="all, delete-orphan")

class Choices(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))

    question = relationship("Questions", back_populates="choices")
