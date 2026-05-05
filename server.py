from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 1. Registro de Usuarios
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    # Hashear la contraseña
    hashed_pw = generate_password_hash(contraseña)

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO usuarios (usuario, password) VALUES (?, ?)', (usuario, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

# 2. Inicio de Sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    conn = get_db_connection()
    user_db = conn.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()
    conn.close()

    if user_db and check_password_hash(user_db['password'], contraseña):
        return jsonify({"mensaje": "Login exitoso. Autenticado."}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# 3. Gestión de Tareas
@app.route('/tareas', methods=['GET'])
def tareas():

    return "<h1>Bienvenido a tu Gestor de Tareas</h1><p>Acá podrás ver tus tareas pendientes.</p>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)