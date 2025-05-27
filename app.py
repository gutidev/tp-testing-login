from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Usuario y contraseña hardcodeados para ejemplo
USUARIO = 'admin'
CONTRASENA = '1234'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['username']
    contrasena = request.form['password']
    if usuario == USUARIO and contrasena == CONTRASENA:
        return f'Bienvenido, {usuario}!'
    else:
        return 'Usuario o contraseña incorrectos', 401

if __name__ == '__main__':
    app.run(debug=True)

