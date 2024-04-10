import random



# Need to consider adding in threading such that each user joining dispatches a thread to handle player actions. each thread is under a main thread that operates at the lobby level?
class Lobby:
    def __init__(self) -> None:
        """ Initialize lobby with random generated ID  and assign unique token for each wobsocket connection """
        self.id_count = 0
        self.users = {}

    def get_random_lobby_id(self):
        """ Get random generated lobby code of size 5 """
        code = []

        for i in range(5):
            char = random.randint(60, 132)
            char = chr(char)
            code.append(char)
        return code
    
    def assign_user_id(self, username):
        self.users[id] = username
        
        