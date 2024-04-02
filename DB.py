from flask_sqlalchemy import SQLAlchemy
from Backend_Entry import db



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250), nullable=False)
    anwser = db.Column(db.String(250), nullable=False)


class DatabaseOperations:
    def add_question(self, Q, A):
        new_question = Question(question=Q, answer=A)
        db.session.add(new_question)
        db.session.commit()

    def delete_question(self, question_id):
        question = Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()

    def delete_question(self, question_id):
        question = Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()

    def get_question_by_id(self, question_id):
        question = Question.query.get(question_id)
        return question

    def get_all_questions(self):
        questions = Question.query.all()
        return questions

    def get_random_question(self):
        import random
        questions = Question.query.all()
        if questions:
            return random.choice(questions)
        return None


