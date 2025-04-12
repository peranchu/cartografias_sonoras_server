from app import create_app
from app.routes.socket import socketio


if __name__ == "__main__":
    app = create_app()
    #app.run(host= '0.0.0.0', port=4000)  #Server desplegado
    #app.run(debug=True, port=4000)  #Server en producción
    socketio.run(app, debug=True, port=5000)
    #socketio.run(app, host= '0.0.0.0', port=5000)

    
