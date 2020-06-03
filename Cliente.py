import socketio
from math import inf as infinity
from inteligencia import ai

sio = socketio.Client()

class GameControl:
    def __init__(self):
        self.username = ""
        self.tid = ""
        self.depth = 0

@sio.on('connect')
def onConnect():
    print('Connection')
    sio.emit('signin', {
        'user_name': game.username,
        'tournament_id': game.tid,
        'user_role': 'player'
    }) 

@sio.on('ready')
def onReady(data):
    move = ai(data['board'], data['player_turn_id'], game.depth)
    print(move)
    sio.emit('play', {
        'player_turn_id': data['player_turn_id'],
        'tournament_id': game.tid,
        'game_id': data['game_id'],
        'movement': [move[0], move[1]]
    })

@sio.on('finish')
def on_finish(data):
    if (data['player_turn_id'] != data['winner_turn_id']):
        print('PERDISTE :(')
    else:
        print('¡GANASTE!')

    sio.emit('player_ready', {
        'tournament_id': game.tid,
        'game_id': data['game_id'],
        'player_turn_id': data['player_turn_id']
    })

@sio.event
def disconnect():
    print('disconnected from data')

@sio.on('ok_signin')
def ok_signin():
    print('Successfully signed in!')


game = GameControl()
game.username = input("Ingresa usuario: ")
game.tid = input("TID: ")
game.depth = int(input('depth: '))
# host = input("Ingrese el host: ")
host = 'http://3.17.150.215:9000'
#host = 'http://localhost:4000'

#sio.connect('http://3.12.129.126:4000')

sio.connect(host)