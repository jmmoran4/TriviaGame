from flask import Flask, jsonify
from DB import DatabaseOperations

app = Flask(__name__)
db_ops = DatabaseOperations()

@app.route('/')
def home():
    
    return 'Hello, Trivia Game!'

@app.route('/add')
def add_question(Q, A):
    try:
        db_ops.add_question(Q, A)
    except Exception as ex:
        print(f"Failed to add question: {ex}")
        return f"Failed to add question: {ex}"

    return 'Question added successfully!'

@app.route('/question/<question_id>')
def delete_question(question_id):
    try:
         db_ops.delete_question(question_id)
    except Exception as ex:
        print(f"Failed to delete question: {ex}")
    

@app.route('/question/<question_id>')
def get_question(question_id):
    try:
        question = db_ops.get_question_by_id(question_id)
    except Exception as ex:
        print(f"Failed to retrieve question: {ex}")
        return jsonify(f"Failed to retrieve question: {ex}")
    
    return jsonify(question)

@app.route('/question/<question_id>')
def get_all_question(question_id):
    try:
        questions = db_ops.get_all_questions(question_id)
    except Exception as ex:
        print(f"Failed to retrieve all questions: {ex}")
        return jsonify(f"Failed to retrieve all questions: {ex}")
    return jsonify(questions)

@app.route('/random')
def get_random_question():
    try:
        question = db_ops.get_random_question()
    except Exception as ex:
        print(f"Failed to retrieve question: {ex}")
        return f"Failed to retrieve question: {ex}"
    return jsonify(question)



if __name__ == '__main__':
    app.run(debug=True)