import streamlit as st
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

st.set_page_config(page_title="Quiz App", layout="centered")
st.title("Quiz Manager (CRUD)")

db = next(get_db())

menu = st.sidebar.selectbox("Choose Action", ["Add Question", "View Questions", "Update Question", "Delete Question", "doquiz"])

# Add Question
if menu == "Add Question":
    st.header("Add New Question")
    question_text = st.text_input("Question:")
    choices = []
    for i in range(4):
        col1, col2 = st.columns([3, 1])
        with col1:
            choice = st.text_input(f"Choice {i + 1}")
        with col2:
            is_correct = st.checkbox("Correct?", key=f"chk_{i}")
        choices.append({"choice_text": choice, "is_correct": is_correct})

    if st.button("Submit"):
        if not question_text or any(c['choice_text'] == '' for c in choices):
            st.warning("Fill all fields.")
        else:
            question = models.Questions(question_text=question_text)
            db.add(question)
            db.commit()
            db.refresh(question)

            for c in choices:
                choice = models.Choices(
                    choice_text=c["choice_text"],
                    is_correct=c["is_correct"],
                    question_id=question.id
                )
                db.add(choice)
            db.commit()
            st.success("Question added!")

# View Questions
elif menu == "View Questions":
    st.header("All Questions")
    questions = db.query(models.Questions).all()
    for q in questions:
        st.subheader(f"{q.id}. {q.question_text}")
        for ch in q.choices:
            mark = "✅" if ch.is_correct else ""
            st.write(f"- {ch.choice_text} {mark}")

# Update Question
elif menu == "Update Question":
    st.header("Update Question")
    question_ids = [q.id for q in db.query(models.Questions).all()]
    if question_ids:
        selected_id = st.selectbox("Select Question ID", question_ids)
        q = db.query(models.Questions).filter_by(id=selected_id).first()

        new_q_text = st.text_input("New Question Text", value=q.question_text)

        updated_choices = []
        for idx, ch in enumerate(q.choices):
            col1, col2 = st.columns([3, 1])
            with col1:
                ch_text = st.text_input(f"Choice {idx + 1}", value=ch.choice_text, key=f"ch_txt_{idx}")
            with col2:
                ch_correct = st.checkbox("Correct?", value=ch.is_correct, key=f"ch_chk_{idx}")
            updated_choices.append({"choice_text": ch_text, "is_correct": ch_correct})

        if st.button("Update"):
            q.question_text = new_q_text
            db.query(models.Choices).filter(models.Choices.question_id == selected_id).delete()
            for c in updated_choices:
                new_ch = models.Choices(
                    choice_text=c["choice_text"],
                    is_correct=c["is_correct"],
                    question_id=q.id
                )
                db.add(new_ch)
            db.commit()
            st.success("Updated successfully!")
    else:
        st.warning("No questions to update.")

# Delete Question
elif menu == "Delete Question":
    st.header("Delete Question")
    question_ids = [q.id for q in db.query(models.Questions).all()]
    if question_ids:
        selected_id = st.selectbox("Select Question ID to Delete", question_ids)
        if st.button("Delete"):
            db.query(models.Choices).filter(models.Choices.question_id == selected_id).delete()
            db.query(models.Questions).filter(models.Questions.id == selected_id).delete()
            db.commit()
            st.success("Deleted successfully!")
    else:
        st.warning("No questions to delete.")

elif menu == "doquiz":
    st.header("Do Quiz")
    questions = db.query(models.Questions).all()
    if questions:
        score = 0
        user_answers = {}

        # Display questions and choices
        for q in questions:
            st.subheader(q.question_text)
            user_answers[q.id] = []
            for ch in q.choices:
                if st.checkbox(ch.choice_text, key=f"chk_{q.id}_{ch.id}"):
                    user_answers[q.id].append(ch.id)

        # Submit button to calculate score
        if st.button("Submit Quiz"):
            for q in questions:
                correct_choices = {ch.id for ch in q.choices if ch.is_correct}
                selected_choices = set(user_answers[q.id])
                if correct_choices == selected_choices:
                    score += 1

            st.success(f"Your score: {score}/{len(questions)}")
    else:
        st.warning("No questions available.")
