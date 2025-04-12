"""
COMUNICACIÓN SOCKET CON MAX/MSP CLIENTES JAVASCRIPT
"""
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
    emit('repro_init_max', message_repro, broadcast=True) # Envío Max nombre del fichero de audio
# -------------------------------------

# Mensaje que recibe desde Max
# parada Audio
@socketio.on('max_msg_estado')
def max_msg(message_max):
    if(message_max == 1):
        emit('max_play', message_max, broadcast=True) # Envío al cliente "fullscreen.js"
        print(message_max)
    if(message_max == 0):
        emit('max_stop', message_max, broadcast=True) # Envío al cliente "fullscreen.js"
        print(message_max)    
# -------------------------------------------

