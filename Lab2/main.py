from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# 📦 Pydantic Schemas
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

class QuestionUpdate(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

# 📦 Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# ✅ Create Question
@app.post('/questions/')
def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)
    db.commit()
    return {"message": "Question created successfully."}

# 🔍 Read Question by ID
@app.get('/questions/{question_id}')
def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Question not found')
    return result

# 🔍 Read Choices for a Question
@app.get('/choices/{question_id}')
def read_choices(question_id: int, db: db_dependency):
    choices = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not choices:
        raise HTTPException(status_code=404, detail='Choices not found')
    return choices

# 📝 Update Question and Choices
@app.put('/questions/{question_id}')
def update_question(question_id: int, updated_question: QuestionUpdate, db: db_dependency):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Update question text
    question.question_text = updated_question.question_text
    db.commit()

    # Delete old choices
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    db.commit()

    # Add new choices
    for choice in updated_question.choices:
        new_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=question_id
        )
        db.add(new_choice)
    db.commit()

    return {"message": "Question updated successfully."}

# ❌ Delete Question (and its choices)
@app.delete('/questions/{question_id}')
def delete_question(question_id: int, db: db_dependency):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Delete choices first (optional if using ON DELETE CASCADE)
    db.query(models.Choices).filter(models.Choices.question_id == question_id).delete()
    db.delete(question)
    db.commit()
    return {"message": "Question and choices deleted successfully."}
