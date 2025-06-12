
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Servidor IDEX funcionando."

@app.route('/api/registro', methods=['POST'])
def registrar():
    data = request.json
    usuario = data.get('usuario')
    email = data.get('email')
    contrasena = data.get('contrasena')

    if not usuario or not email or not contrasena:
        return jsonify({'error': 'Faltan datos'}), 400

    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            usuarios = json.load(f)
    else:
        usuarios = []

    if any(u['usuario'] == usuario for u in usuarios):
        return jsonify({'error': 'El usuario ya existe'}), 400

    usuarios.append({'usuario': usuario, 'email': email, 'contrasena': contrasena})

    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=2)

    return jsonify({'mensaje': 'Usuario registrado con éxito'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            usuarios = json.load(f)
    else:
        usuarios = []

    if any(u['usuario'] == usuario and u['contrasena'] == contrasena for u in usuarios):
        return jsonify({'mensaje': 'Login exitoso'})
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
