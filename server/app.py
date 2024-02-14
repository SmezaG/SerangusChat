# /SerangusChat/server/app.py

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'))
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia esto por una clave secreta segura
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Solicitar nombre de usuario al conectarse
    emit('request_username')

@socketio.on('username_response')
def handle_username_response(data):
    # Asignar nombre de usuario a la sesión y notificar a los demás usuarios
    session['username'] = data['username']
    emit('user_connected', {'username': session['username']}, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    # Enviar mensaje con nombre de usuario
    emit('message', {'username': session['username'], 'message': msg['message']}, broadcast=True)
    # emit("message",{'username': "abc", 'message': "cde"},broadcast=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
