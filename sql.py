from flask import Flask, request
import sqlite3
import hashlib

app = Flask(__name__)
db_name = 'usuarios.db'

# Diccionario con los integrantes del grupo y las contraseñas a elección
integrantes = {
    "Gabriel Leon": "Duoc2027",
    "Daniel Leon": "Duoc2026",
}

def inicializar_db():
    """Crea la base de datos y almacena los usuarios con contraseñas en hash"""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Crear la tabla si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
                 (USERNAME TEXT PRIMARY KEY NOT NULL,
                  HASH TEXT NOT NULL);''')
    
    # Insertar cada integrante en la base de datos
    for usuario, clave in integrantes.items():
        # Hashear la contraseña usando SHA-256
        hash_value = hashlib.sha256(clave.encode()).hexdigest()
        try:
            c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)", (usuario, hash_value))
        except sqlite3.IntegrityError:
            # Si el usuario ya existe, simplemente lo ignora y continúa
            pass 
            
    conn.commit()
    conn.close()

# Ruta principal que muestra el formulario HTML
@app.route('/', methods=['GET'])
def index():
    return '''
        <h2>Login de Usuarios - Examen Transversal DRY7122</h2>
        <form action="/login" method="post">
            Usuario: <input type="text" name="username"><br><br>
            Contraseña: <input type="password" name="password"><br><br>
            <input type="submit" value="Validar Usuario">
        </form>
    '''

# Ruta para procesar el inicio de sesión y validar el hash
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USER_HASH WHERE USERNAME = ?", (username,))
    records = c.fetchone()
    conn.close()
    
    if not records:
        return f"<h3>[!] Error: El usuario '{username}' no se encuentra registrado en la base de datos.</h3>"
    
    db_hash = records[0]
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if db_hash == input_hash:
        return f"<h3>[+] Validación exitosa. ¡Bienvenido al sistema, {username}!</h3>"
    else:
        return f"<h3>[-] Error: Contraseña incorrecta para el usuario '{username}'.</h3>"

if __name__ == '__main__':
    inicializar_db()
    print("Base de datos inicializada y usuarios cargados.")
    print("Iniciando servidor web Flask en el puerto 7500...")
    # Configurado en el puerto 7500
    app.run(host='0.0.0.0', port=7500)