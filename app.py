from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Necesario para usar flash
app.secret_key = 'clave_secreta'  

# Usuario y contraseña hardcodeados para ejemplo
USUARIO = 'admin'
CONTRASENA = '1234'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/status', methods=['POST'])
def status():
    usuario = request.form['username']
    contrasena = request.form['password']
    if usuario != USUARIO:
        error_usuario = 'El usuario no es correcto'
        return render_template('login.html', error_usuario=error_usuario, username=usuario)

    if contrasena != CONTRASENA:
        error_contrasena = 'La contraseña es incorrecta'
        return render_template('login.html', error_contrasena=error_contrasena, username=usuario)

    # Si todo está OK, mostrar status
    return render_template('status.html', nombre=usuario)


@app.route('/status')
def status_get():
    return render_template('status.html')




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

    # Guardar en base de datos u otra lógica...
    return render_template('status.html', nombre=nombre)

def es_valido(nombre, email, password):
    return True




@app.route('/change_password')
def change_password():
    return render_template('changePassword.html')

@app.route('/change_password', methods=['POST'])
def change_password_post():
    if request.method == 'POST':
        actual = request.form['currentPassword']
        nueva = request.form['newPassword']
        confirmar = request.form['confirmPassword']

        CONTRASENA_ACTUAL = '1234'  # Simulado

        if actual != CONTRASENA_ACTUAL:
            return render_template('changePassword.html', error='La contraseña actual no es correcta.')

        if nueva != confirmar:
            return render_template('changePassword.html', error='Las contraseñas nuevas no coinciden.')

        if len(nueva) < 6:
            return render_template('changePassword.html', error='La nueva contraseña debe tener al menos 6 caracteres.')

        # Aquí deberías guardar la nueva contraseña en tu base de datos

        #return render_template('changePassword.html', success='Contraseña actualizada correctamente.')
        flash('Contraseña actualizada correctamente.')
        return redirect(url_for('login'))


    return render_template('changePassword.html')



if __name__ == '__main__':
    app.run(debug=True)

