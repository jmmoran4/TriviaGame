from pymongo import MongoClient
from bson.objectid import ObjectId
import random

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017')
db = client.trivia_database
Q_A_collection = db.questions
lobby_collection = db.lobbies
class DatabaseOperations:
    def add_question(self, QA):
        """ Add new question(Q) with a matching answer(A) """
        Q_A_collection.insert_one(QA)

    def delete_question(self, Q_A_ID):
        """ Delete question and answer (Q_A) """
        Q_A_collection.delete_one({"_id": ObjectId(Q_A_ID)})

    def get_question_by_id(self, Q_A_ID):
        """ Retrieve question and answer (Q_A_ID) """
        return Q_A_collection.find_one({"_id": ObjectId(Q_A_ID)})

    def get_all_questions(self):
        """ Return a list of all questions and answers from DB """
        return list(Q_A_collection.find())

    def get_random_question(self):
        """ Return a random question and answer from db or None if it's empty """
        Q_As = list(Q_A_collection.find())
        return random.choice(Q_As) if Q_As else None

    def update_question(self, newQ, newA, new_IncorrectA, oldID):
        """ Change existing question with (newQ, newA), and delete old question (oldID)"""
        newQA = self.get_question_by_id(oldID)
        newQA['question'] = newQ
        newQA['correct_answer'] = newA
        newQA['incorrect_answers'] = new_IncorrectA
        self.delete_question(oldID)
        self.add_question(newQA)        

    def get_question_by_type(self, category, quesitonCache):
        pipeline = [
        {'$match': {"category": category}},
        {'$sample': {'size': 1}}  # You can adjust the 'size' for more than one random document
        ]
        Qs = list(Q_A_collection.aggregate(pipeline))
        Q = Qs[random.randint(0, len(Qs)-1)]

        while Q in quesitonCache:
            Q = Qs[random.randint(0, len(Qs)-1)]
        return Q

    def get_lobby(self, lobbyID):
        """ Get a lobby and its content with lobbyID """
        return lobby_collection.find_one({"_id": ObjectId(lobbyID)})