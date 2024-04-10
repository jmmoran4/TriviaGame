import DB as db
from flask import Flask
from operator import itemgetter
from flask_login import LoginManager
import sys

user_collection = db['users']
leaderboard = db['leaderboard']
rooms_collection = db['rooms']
lobby_collection = db['lobbies']

# add user as {'username' : username, 'wins' : '0', 'loss' : '0'}


def add_user(username, password):
    record = {'username': username, 'password': password, 'wins': 0, 'loss': 0, 'draw': 0}
    user_collection.insert_one(record)
    leaderboard.insert_one({username: 0})


def check_for_user(username):
    result = user_collection.find_one({'username': username})
    if result is not None:
        return result
    else:
        return None


def update_password(username, password):
    user = user_collection.find_one({'username': username})
    wins = user['wins']
    losses = user['loss']
    draws = user['draw']
    new_record = {'$set': {'username': username, 'password': password, 'wins': wins, 'loss': losses, 'draw': draws}}
    user_collection.update_one({'username': username}, new_record)


# add a win or loss to the users stats


def update_player_stats(username: str, stat_to_change: str, increment: int):
    record = user_collection.find_one({'username': username})
    wins = record['wins']
    loss = record['loss']
    draws = record['draw']
    if stat_to_change == 'wins':
        wins += increment
    elif stat_to_change == 'loss':
        loss += increment
    elif stat_to_change == 'draw':
        draws += increment
    new_record = {'$set': {'username': username, 'wins': wins, 'loss': loss, 'draw': draws}}
    user_collection.update_one({'username': username}, new_record)
    update_leaderboard(record['username'])
# change users score to {'username' : username, 'score' : new_score}... or insert if not there
# score will be an integer that ranks the player based on # games played and W/L ratio


def update_leaderboard(username):
    user = user_collection.find_one({'username': username})
    old_record = leaderboard.find({})
    old_score = None
    for record in old_record:
        data = record.popitem()
        if data[0] == user['username']:
            old_score = data[1]
    games_played = user['wins'] + user['loss']
    win_loss = user['wins'] - user['loss']
    new_score = 0
    if win_loss > 0:
        new_score = games_played * win_loss
    else:
        new_score = games_played * 0.5
    new_record = {'$set': {user['username']: new_score}}
    leaderboard.update_one({user['username']: old_score}, new_record)


# returns a dictionary of form {rank : [score, username]}


def get_leaderboard():
    records = leaderboard.find({})
    record_list = []
    # add all the users to a List of List to be sorted by score
    for record in records:
        item = record.popitem()
        username = item[0]
        score = int(item[1])
        record_list.append([score, username])
    sorted_list = sorted(record_list, key=itemgetter(0))
    return_leaderboard = {}
    rank = len(record_list)
    for user in sorted_list:
        return_leaderboard[rank] = user
        rank -= 1
    return return_leaderboard


def drop(collection):
    collection.drop()


def assign_room(username, room):
    record = {'username': username, 'room': room}
    if get_users_room(username) is not None:
        rooms_collection.update_one({'username': username}, {"$set": record})
    else:
        rooms_collection.insert_one(record)


def get_users_room(username):
    return rooms_collection.find_one({'username': username})


def delete_rooms():
    rooms_collection.delete_many({})


def create_lobby(lobby, username):
    lobby_collection.insert_one({'lobby': lobby, 'user1': username})


def get_lobbies():
    lobbies = list(lobby_collection.find({}))
    ret_val = []
    for lobby in lobbies:
        ret_val.append(lobby.get('lobby'))
    return ret_val


def get_lobby(username):
    return lobby_collection.find_one({'user1': username})


def delete_lobby(lobby):
    lobby_collection.delete_one({'lobby': lobby})



def delete_lobbies():
    lobby_collection.delete_many({})