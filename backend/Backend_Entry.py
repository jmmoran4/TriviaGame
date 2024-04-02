from flask import Flask, jsonify
from backend.DB import DatabaseOperations
from flask import request
app = Flask(__name__)
db_ops = DatabaseOperations()

@app.route('/')
def home():
    
    return 'Hello, Trivia Game!'

@app.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    Q = data.get('question')
    A = data.get('answer')
    try:
        db_ops.add_question(Q, A)
    except Exception as ex:
        print(f"Failed to add question: {ex}")
        return jsonify({ 'message':f"Failed to add question: {ex}"}), 

    return jsonify({'message':'Question added successfully!'})

@app.route('/question/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
         db_ops.delete_question(question_id)
         return jsonify({'message': 'Question deleted successfully'}), 200
    except Exception as ex:
        print(f"Failed to delete question: {ex}")
        return jsonify({'message': 'Question not deleted properly'}), 409

@app.route('/question/<question_id>', methods=['GET'])
def get_question(question_id):
    question = db_ops.get_question_by_id(question_id)
    if question:
        return jsonify(question), 200
    else:
        print(f"Failed to retrieve question")
        return jsonify({'message':f"Failed to retrieve question"}), 404

@app.route('/questions/all/<question_id>', methods=['GET'])
def get_all_question(question_id):
    try:
        questions = db_ops.get_all_questions(question_id)
    except Exception as ex:
        print(f"Failed to retrieve all questions: {ex}")
        return jsonify({'message':f"Failed to retrieve all questions: {ex}"})
    return jsonify(questions)

@app.route('/questions/random', methods=['GET'])
def get_random_question():
    try:
        question = db_ops.get_random_question()
    except Exception as ex:
        print(f"Failed to retrieve question: {ex}")
        return jsonify({'message':f"Failed to retrieve question: {ex}"})
    return jsonify(question)

@app.route('/quesitons/<question_id>', methods=['PUT'])
def update_question(newQ, newA, oldID):
    try:
        db_ops.update_question(newQ, newA)
    except Exception as ex:
        print(f"Failed to update quesiton: {ex}")
        return jsonify({'message': f"Failed to update quesiton: {ex}"})
    return jsonify({'message':'Quesiton updated successfully'})


if __name__ == '__main__':
    app.run(debug=True)