import unittest
from DB import DatabaseOperations, Q_A_collection, lobby_collection
from bson.objectid import ObjectId


class TestDatabaseOperations(unittest.TestCase):
    
    def setUp(self):
        self.db_ops = DatabaseOperations()
        self.mock_question = {
            "type":"multiple","difficulty":"medium","category":"Sports",
            "question":"What national team won the 2016 edition of UEFA European Championship?",
            "correct_answer":"Portugal","incorrect_answers":["France","Germany","England"]
                              }
        self.added_question = Q_A_collection.insert_one(self.mock_question).inserted_id

    def test_add_question(self):
        self.db_ops.add_question({"type":"multiple","difficulty":"medium","category":"Sports","question":"How many scoring zones are there on a conventional dart board?","correct_answer":"82","incorrect_answers":["62","42","102"]})
        added_Q_A = Q_A_collection.find_one({"question":"How many scoring zones are there on a conventional dart board?"})
        print(self.assertIsNotNone(added_Q_A))
        self.assertEqual(added_Q_A['correct_answer'], "82")

    def test_delete_question(self):
        self.db_ops.delete_question(self.added_question)
        deleted_Q_A = Q_A_collection.find_one({"_id": self.added_question})
        self.assertIsNone(deleted_Q_A)

    def test_get_question_by_id(self):
        Q_A = self.db_ops.get_question_by_id(self.added_question)
        self.assertIsNotNone(Q_A)
        self.assertEqual(Q_A['correct_answer'], self.mock_question['correct_answer'])

    def test_get_all_questions(self):
        questions = self.db_ops.get_all_questions()
        self.assertIsInstance(questions, list)
        self.assertTrue(len(questions) > 0)

    def test_get_random_question(self):
        random_Q_A = self.db_ops.get_random_question()
        self.assertIsNotNone(random_Q_A)
        self.assertIn('question', random_Q_A)
        self.assertIn('correct_answer', random_Q_A)

    def test_update_question(self):
        new_Q = "What is the smallest planet?"
        new_A = "Mercury"
        new_IncorrectA = ["US", "Canada", "France"]
        self.db_ops.update_question(new_Q, new_A, new_IncorrectA, self.added_question)
        updated_Q_A = Q_A_collection.find_one({"question": new_Q})
        self.assertIsNotNone(updated_Q_A)
        self.assertEqual(updated_Q_A['correct_answer'], new_A)

    def test_get_lobby(self):
        lobby_id = lobby_collection.insert_one({"name": "Test Lobby"}).inserted_id
        lobby = self.db_ops.get_lobby(lobby_id)
        self.assertIsNotNone(lobby)
        self.assertEqual(lobby['name'], "Test Lobby")

if __name__ == '__main__':
    unittest.main()
