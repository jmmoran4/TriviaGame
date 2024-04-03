import json
from DB import DatabaseOperations
import hashlib
class FileIO:
    def __init__(self) -> None:
        self.db_ops = DatabaseOperations()

    def add_entries(self, path):
        rawData = ""
        with open(path, 'r') as f:
            for line in f:
                rawData += line
        
        mainDict = {}
        try:
            mainDict = json.loads(rawData)
        except Exception as ex:
            print(ex, f'------{rawData[224]}-----')
        for dict in mainDict['results']:
            QA = {
                'type': dict['type'],
                'difficulty': dict['difficulty'],
                'category': dict['category'],
                'question': dict['question'],
                'correct_answer': dict['correct_answer'],
                'incorrect_answers': dict['incorrect_answers']
            }
            QA['ID'] = self.hash_dict(QA)
            self.db_ops.add_question(QA)
            
    def hash_dict(self, d):
        """Create a SHA-256 hash of a dictionary."""
        d_hash = hashlib.sha256()
        encoded = json.dumps(d, sort_keys=False).encode()
        d_hash.update(encoded)
        return d_hash.hexdigest()

if __name__ == '__main__':
    F = FileIO()
    F.add_entries('GameData/GENRAL_KNOWLEDGE_MULTPILECHOICE_HARD.txt')
    F.add_entries('GameData/HISTORY_MULTIPLECHOICE_HARD.txt')
    F.add_entries('GameData/GEOGRAPHY_MULTIPLECHOICE_HARD.txt')
    F.add_entries('GameData/SCIENCE_COMPUTERS_MULTIPLECHOICE_MEDIUM.txt')
    F.add_entries('GameData/SPORTS_MULTIPLECHOICE_MEDIUM.txt')