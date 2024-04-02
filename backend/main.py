try:
    from flask import Blueprint, render_template, redirect, url_for
    from flask import request
    from flask_login import login_required, current_user
    import DB as db
    import globals as globals
    from flask_socketio import emit, join_room, leave_room
    import flask_socketio
    import asyncio
    import json
    import sys
    import time
except Exception as e:
    print(" Some pacakages are missing: {}".format(e))

main = Blueprint('main', __name__)

global counter
counter = 0


@main.route('/')
def index():
    return render_template('../frontend/start.html')


@main.route('/profile')
@login_required
def profile():
    users_data = db.check_for_user(current_user.username)
    return render_template('profile.html', name=current_user.username, wins=users_data.get('wins'),
                           draws=users_data.get('draw'), losses=users_data.get('loss'))


@main.route('/game')
@login_required
def game():
    return render_template('eric_html_files/screen_one.html')


@main.route('/waiting_room/<waiting_room_id>')
@login_required
def waiting_room(waiting_room_id):
    # Create Lobby 
    if '/waiting_room/' + waiting_room_id not in db.get_lobbies():
        db.create_lobby('/waiting_room/' + str(waiting_room_id))
    # If the lobby already exists remove it as we don't want more than 2 people per lobby
    else:
        db.delete_lobby('/waiting_room/' + waiting_room_id)
    return render_template('waiting_room.html')


@main.route('/game_over/X')
@login_required
def game_over_x():
    return render_template('game_over.html', game_winner="X")


@main.route('/game_over/O')
@login_required
def game_over_o():
    return render_template('game_over.html', game_winner="O")


@main.route('/draw_game')
@login_required
def draw_game():
    return render_template('draw_game.html')


@main.route('/board/<game_id>')
@login_required
def board(game_id):
    db.assign_room(current_user.username, game_id)
    # Create Lobby 
    if '/board/' + game_id not in db.get_lobbies():
        db.create_lobby('/board/' + str(game_id), current_user.username)
    # If the lobby already exists remove it as we don't want more than 2 people per lobby
    else:
        db.delete_lobby('/board/' + game_id)
    return render_template('eric_html_files/screen_two.html')


@main.route('/leaderboard')
@login_required
def leaderboard():
    all_users_data_dict = db.get_leaderboard()
    rank = []
    record = []

    for key in all_users_data_dict:
        rank.append(rank)
        record.append(all_users_data_dict[key])

    record.reverse()

    return render_template('leaderboard.html', win_loss_list=record)


@main.route('/lobbies')
@login_required
def lobbies():
    active_lobbies = db.get_lobbies()
    return render_template('lobbies.html', created_lobbies = active_lobbies)


@globals.socketsio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})
    sid = request.sid
    # Get the room for the current user
    room = db.get_users_room(current_user.username).get('room')
    # Get the current users lobby information
    user1 = db.get_lobby(current_user.username)
    # If the user is user1 then they are player 'X'
    if user1 is not None and current_user.username == user1.get('user1'):
        join_room(str(room))
        emit('state and player and room', {'State': 1, 'Player': 'X', 'Room': room})
    else:
        join_room(str(room))
        emit('state and player and room', {'State': 0, 'Player': 'O', 'Room': room})



@globals.socketsio.on('player move')
def test_messages(msg):
    room = db.get_users_room(current_user.username).get('room')
    emit('opponent move', msg, to=str(room), include_self=False)


@globals.socketsio.on('win')
def player_win(msg):
    room = db.get_users_room(current_user.username).get('room')
    # if msg.get('player') != None:
    db.update_player_stats(current_user.username, 'wins', 1)
    # elif msg.get('otherPlayer') != None:
        # db.update_player_stats(current_user.username, 'loss', 1)
    emit('Winner', msg, to=str(room), include_self=False)


@globals.socketsio.on('loss')
def player_loss(msg):
    room = db.get_users_room(current_user.username).get('room')
    db.update_player_stats(current_user.username, 'loss', 1)
    emit('Loser', msg, to=str(room), include_self=False)


@globals.socketsio.on('draw')
def draw(msg):
    room = db.get_users_room(current_user.username).get('room')
    db.update_player_stats(current_user.username, 'draw', 1)
    emit("Draw", msg, to=str(room), include_self=False)


@globals.socketsio.on('disconnected')
def disconnect():
    pass