from pymongo import MongoClient
from bson.objectid import ObjectId
import random

# MongoDB connection setup
client = MongoClient('your_mongodb_connection_string')
db = client.trivia_database
Q_A_collection = db.questions

class DatabaseOperations:
    def add_question(self, Q, A):
        """ Add new question(Q) with a matching answer(A) """
        Q_A = {
            "question": Q,
            "answer": A
        }
        Q_A_collection.insert_one(Q_A)

    def delete_question(self, Q_A_ID):
        """ Delete question and answer (Q_A) """
        Q_A_collection.delete_one({"_id": ObjectId(Q_A_ID)})

    def get_question_by_id(self, Q_A_ID):
        """ Retrieve question and answer (Q_A_ID) """
        return Q_A_collection.find_one({"_id": ObjectId(Q_A_ID)})

    def get_all_questions(self):
        """ Return a list of all questions and answers from DB """
        return list(Q_A_collection.find())

###
    def get_random_question(self):
        """ Return a random question and answer from db or None if it's empty """
        Q_As = list(Q_A_collection.find())
        return random.choice(Q_As) if Q_As else None


