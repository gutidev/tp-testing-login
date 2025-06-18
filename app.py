from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps


# Usuario y contraseña hardcodeados para ejemplo
usuarios_registrados = {
    'admin': 'admin123'
}

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesario para usar flash

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorada


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    session.pop('usuario', None)  # Elimina al usuario de la sesión
    return render_template('login.html')


# Simulación de estados de servicios
estados_servicios = {
    'Operaciones': 'Normal',
    'Base de datos': 'Normal',
    'Web Campus': 'Normal',
    'App Mobile': 'Normal',
    'Biblioteca': 'Normal',
    'Redes': 'Normal',
    'UADE Labs': 'Normal',
    'UADE Hub': 'Normal',
    'UADE Investigación': 'Normal'
}


@app.route('/status', methods=['POST'])
def status():
    usuario = request.form['username']
    contrasena = request.form['password']

    if usuario not in usuarios_registrados:
        error_usuario = 'El usuario no es correcto'
        return render_template('login.html', error_usuario=error_usuario, username=usuario)

    if usuarios_registrados[usuario] != contrasena:
        error_contrasena = 'La contraseña es incorrecta'
        return render_template('login.html', error_contrasena=error_contrasena, username=usuario)

    session['usuario'] = usuario
    return render_template('status.html', nombre=usuario, estados=estados_servicios)


@app.route('/status')
@login_requerido
def status_get():
    nombre = session['usuario']
    return render_template('status.html', nombre=nombre, estados=estados_servicios)



@app.route('/registro')
def registro():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['full-name']
    email = request.form['email']
    password = request.form['password']

    if not es_valido(nombre, email, password):
        error = 'Datos inválidos o incompletos'
        return render_template('register.html', error=error)

    # Guardar usuario en el diccionario (temporal)
    usuarios_registrados[nombre] = password

    session['usuario'] = nombre
    return redirect(url_for('status_get'))


def es_valido(nombre, email, password):
    return True




@app.route('/change_password')
def change_password():
    usuario = session.get('usuario')
    return render_template('changePassword.html', usuario=usuario)

@app.route('/change_password', methods=['POST'])
def change_password_post():
    username = request.form['username']
    nueva = request.form['newPassword']
    confirmar = request.form['confirmPassword']
    if username not in usuarios_registrados:
        return render_template('changePassword.html', error='El usuario no existe.')
    if nueva != confirmar:
        return render_template('changePassword.html', error='Las contraseñas no coinciden.')
    if len(nueva) < 6:
        return render_template('changePassword.html', error='La nueva contraseña debe tener al menos 6 caracteres.')
    # Actualizar contraseña
    usuarios_registrados[username] = nueva
    flash('Contraseña actualizada correctamente.')
    return redirect(url_for('login'))


@app.route('/reportar_incidente', methods=['POST'])
@login_requerido
def reportar_incidente():
    servicio = request.form['servicio']
    detalle = request.form['detalle']
    if servicio in estados_servicios:
        estados_servicios[servicio] = 'Incidencia Reportada'
    return redirect(url_for('status_get'))


@app.route('/restablecer_estado', methods=['POST'])
@login_requerido
def restablecer_estado():
    if session.get('usuario') != 'admin':
        return "No autorizado", 403
    servicio = request.form['servicio']
    if servicio in estados_servicios:
        estados_servicios[servicio] = 'Normal'
    return redirect(url_for('status_get'))



@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Elimina al usuario de la sesión
    flash('Sesión cerrada correctamente.')  # Muestra mensaje
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

