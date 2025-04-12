"""
MODELOS PARA ESCRITURA Y LECTURA DE LA Bd
"""
from app.utils.db import db  # importa la instancia a la Db


# Modelo posiciones
class Posiciones(db.Model):
    # Atributos
    rowid = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(precision=16), nullable=False)
    longitude = db.Column(db.Float(precision=16), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    audio_name = db.Column(db.String, nullable=False)

    #CONSTRUCTOR
    def __init__(self, latitude, longitude, name, date, time, audio_name):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.date = date
        self.time = time
        self.audio_name = audio_name

    # MÉTODOS 
    # Sobre escritura método String para la clase Posiciones
    def __str__(self):
        return "\nlatitude: {}. longitude: {}. name: {}. date: {}. time: {}. audio_name: {}.\n".format(
            self.latitude, self.longitude, self.name, self.date, self.time, self.audio_name
        )

    # Serializa los datos de la tabla para comvertirlos a JSON
    def Serialize(self):
        return {
            "rowid": self.rowid,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name,
            "date": self.date,
            "time": self.time,
            "audio_name": self.audio_name
        }
