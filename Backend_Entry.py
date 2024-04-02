from flask import Flask, jsonify
from DB import DatabaseOperations

app = Flask(__name__)
db_ops = DatabaseOperations()

@app.route('/')
def home():
    
    return 'Hello, Trivia Game!'

@app.route('/add')
def add_question(Q, A):
    db_ops.add_question(Q, A)
    return 'Question added successfully!'

@app.route('/question/<question_id>')
def get_question(question_id):
    question = db_ops.get_question_by_id(question_id)
    return jsonify(question)

@app.route('/random')
def get_random_question():
    question = db_ops.get_random_question()
    return jsonify(question)

if __name__ == '__main__':
    app.run(debug=True)