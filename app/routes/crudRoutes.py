"""
RUTAS DEL SERVER
"""
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from os.path import abspath, dirname, join
import os
from os import remove
from werkzeug.utils import secure_filename  #Subida Archivos
from logging import exception  # Manejo exceptciones
from app.Models.modelsCrub import db, Posiciones  # importa Métodos del modelo
from app.utils.db import db
from app.form.formulario import Posiciones_form #Formularios

# Inicia las rutas y configura el prefijo para la api
crud = Blueprint("crud", __name__, url_prefix="/api")

# Rutas de la carpeta Audios
Audio_dir = os.path.abspath(os.getcwd()) + '\\app\\Audios\\'
#print (Audio_dir)

# Archivos permitidos
ALLOWED_EXTENSIONS = {'wav', 'aiff'}

# Separa el Nombre de la extensión del archivo
def allowed_file(nameAudio):
    return '.' in nameAudio and nameAudio.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# RUTAS_______________________________
# Sirve el formulario
# recibe el formulario
@crud.route("/datosPos", methods=["GET", "POST"])
def getDatos():
    form = Posiciones_form()
    # Si es un método POST: Procesa el formulário
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # ----ARCHIVO AUDIO----
                # captura nombre del archivo del formulario
                File = request.files["file"]  
                # comprueba la extensión
                if allowed_file(File.filename):  
                    nameAudio = secure_filename(File.filename)
                    ruta_file = os.path.join(Audio_dir, nameAudio)
                    print(ruta_file)
                else:
                    flash('Archivo no Válido', 'danger')
                    return redirect(url_for('crud.getDatos')) 
                
                # Comprueba que no exista
                if os.path.isfile(ruta_file):
                    flash("El Archivo Ya existe.", 'danger')
                    return redirect(url_for('crud.getDatos'))
                else:
                    File.save(os.path.join(Audio_dir, nameAudio))
               
               #----DATOS-----
                # Recoge los datos del formulario
                latitude = request.form["latitude"]
                longitude = request.form["longitude"]
                name = request.form["name"]
                date = request.form["date"]
                time = request.form["time"]

                # Crea objeto de la clase posiciones con el modelo para la tabla de la Db
                posiciones = Posiciones(
                    float(latitude), float(longitude), name, date, time, nameAudio 
                )
                # Envía a la Bd
                db.session.add(posiciones)
                db.session.commit()

                flash("Archivo Subido","success" )  # mensajes de aviso
                return redirect(url_for('crud.getDatos'))
                #return jsonify(posiciones.Serialize()), 200

            except Exception:
                exception("[SERVER]: Error ->")
                return jsonify({"msg": "Algo Ha salido mal"}), 500  # convierte a JSON
            
    # Si es un método es GET Devuelve el formulário
    if request.method == 'GET':   
        return render_template('formulario.html', form=form)    
# --------------------------------------------------------------------------

# Devuelve todos Los Registros de la Db Para Listarlos
@crud.route("/posiciones/", methods=["GET"])
def getPosiciones():
    try:
        posiciones = Posiciones.query.all()
        return render_template('listar.html', listPosiciones = posiciones), 200
    
    except Exception:
        exception("[SERVER]: Error ->")
        return jsonify({"msg": "Ha ocurrido un error"}), 500  # convierte a JSON
# -----------------------------------------------------------

# Devuelve todos Los Registros de la Db Para Pintarlos en el Mapa JSON
# Llamado desde el "fullScreen.js"
@crud.route("/posicionesMapa", methods=["GET"])
def getPosicionesMapa():
    try:
        posiciones = Posiciones.query.all()
        toReturn = [posicion.Serialize() for posicion in posiciones]

        # Serializa el diccionario
        return jsonify(toReturn), 200  # convierte a JSON
    except Exception:
        exception("[SERVER]: Error ->")
        return jsonify({"msg": "Ha ocurrido un error"}), 500  # convierte a JSON
# -----------------------------------------------------------
    
# Borra todos registros Bd
@crud.route("/delete")
def delete():
    try:
        db.session.query(Posiciones).delete()
        db.session.commit()
        return jsonify({"msg": "Boorados Los registros"}), 200  # convierte a JSON

    except Exception:
        exception("[SERVER]: Error ->")
        return jsonify({"msg": "Ha ocurrido un error"}), 500  # convierte a JSON    

#------------------------------------------

# Borra Registor por ID
# Llamado desde "listar.html"
@crud.route("/delete/<id>", methods=["GET", "POST"])
def deleteId(id):
    try:
        posicion = Posiciones.query.get(id)
        nameAudio = posicion.audio_name

        #Borra el fichero de audio
        url_File = os.path.join(Audio_dir, nameAudio)
        if os.path.exists(url_File):
            remove(url_File)
        else:
            flash("El Archivo no existe.", 'danger')
            return redirect(url_for('posiciones'))
                
        #Borra de la base de Datos
        db.session.delete(posicion)
        db.session.commit()

        flash("Registro Eliminado", 'success')
        return redirect(url_for('crud.getPosiciones'))
    
    except Exception:
        exception("[SERVER]: Error ->")
        return jsonify({"msg": "Ha ocurrido un Error"}), 500


# ----------------------------------

# Vista MAPA FULLSCREEN
@crud.route("/fullScreen", methods=['GET'])
def fullScreen():
    return render_template("fullscreen.html")
# -----------------------------------------------------------

# RutaReproduccion
@crud.route("/repro/<id>", methods=['GET'])
def reproduccion(id):
    try: #filtra por el ide del registro para obtener los datos
        ident = Posiciones.query.filter_by(rowid=id).first()   
        if not ident:
            return jsonify({"msg": "No existe este registro"}), 200
        else:
            datosPosiciones = [
                ident.Serialize()
            ]

            return jsonify(datosPosiciones), 200  # convierte a JSON
        
    except Exception: 
        exception("[SERVER]: Error ->")
        return jsonify({"msg": "Ha ocurrido un Error"}), 500   
# --------------------------------------------------------






