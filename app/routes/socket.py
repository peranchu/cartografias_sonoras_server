from flask_socketio import send, emit
from ..import socketio

#--SOCKETS----
@socketio.on('connect')
def handle_connect():
    print('cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('cliente desconectado') 

# Mensaje enviado a MAX cuando se seleciona una ubicación
@socketio.on('repro_init')
def recibeMsj(message_repro):
    print('recibido mensaje:', message_repro) 
    emit('repro_init_max', message_repro, broadcast=True)

@socketio.on('max_msg')
def max_msg(message_max):
    print(message_max)

