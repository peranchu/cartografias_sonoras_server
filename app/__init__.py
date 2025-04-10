from flask import Flask
from flask_socketio import SocketIO, send, emit
from .routes.crudRoutes import crud
from .utils.db import db
import os


#Ruta absoluta Bd
file_path = os.path.abspath(os.getcwd())+"\\app\\database\\DbCarto.db" 

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    #configura e inicia la Bd 
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + file_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.secret_key = "19721972" # Token para Formularios
    app.config['SECRET_KEY'] ="Texuca" #clave socketio
    app.register_blueprint(crud)    #Registra todas las rutas de la aplicación
    socketio.init_app(app)
    return app









