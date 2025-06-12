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
        return render_template('status.html')
    else:
        return render_template('login.html', error='Usuario o contraseña incorrectos', username=usuario)

@app.route('/registro')
def registro():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

