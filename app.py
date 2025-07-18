from flask import Flask, render_template, request, redirect, flash, jsonify
from db import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = '1234'  # Llave para manejar sesiones y alertas 

# Página principal: muestra la tabla con todos registros de los créditos solicitados
@app.route('/')
def index():
    conn = get_db_connection()
    creditos = conn.execute('SELECT * FROM creditos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', creditos=creditos)

# Ruta para agregar un nuevo crédito desde el formulario del modal
@app.route('/agregar', methods=['POST'])
def agregar_credito():
    # Obtener datos del formulario
    cliente = request.form.get('cliente', '').strip()
    monto = request.form.get('monto', '').strip()
    tasa = request.form.get('tasa', '').strip()
    plazo = request.form.get('plazo', '').strip()
    fecha = request.form.get('fecha', '').strip()

    # Validar que todos los campos estén completos
    if not cliente or not monto or not tasa or not plazo or not fecha:
        flash('Por favor completa todos los campos.', 'danger')
        return redirect('/')

    # Validar que los valores numéricos sean válidos
    try:
        monto = float(monto)
        tasa = float(tasa)
        plazo = int(plazo)
    except ValueError:
        flash('Monto, tasa y plazo deben ser numéricos.', 'danger')
        return redirect('/')

    # Insertar el nuevo crédito en la base de datos
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO creditos (cliente, monto, tasa_interes, plazo, fecha_otorgamiento) VALUES (?, ?, ?, ?, ?)',
        (cliente, monto, tasa, plazo, fecha)
    )
    conn.commit()
    conn.close()

    flash('Crédito creado con éxito.', 'success')
    return redirect('/')

# Ruta para editar un crédito existente
@app.route('/editar', methods=['POST'])
def editar_credito():
    # Obtener datos del formulario
    id_ = request.form.get('id', '').strip()
    cliente = request.form.get('cliente', '').strip()
    monto = request.form.get('monto', '').strip()
    tasa = request.form.get('tasa', '').strip()
    plazo = request.form.get('plazo', '').strip()
    fecha = request.form.get('fecha', '').strip()

    # Validar que todos los campos estén completos
    if not id_ or not cliente or not monto or not tasa or not plazo or not fecha:
        flash('Por favor completa todos los campos para editar.', 'danger')
        return redirect('/')

    # Validar datos numéricos
    try:
        monto = float(monto)
        tasa = float(tasa)
        plazo = int(plazo)
        id_ = int(id_)
    except ValueError:
        flash('Los valores numéricos son inválidos.', 'danger')
        return redirect('/')

    # Actualizar el crédito en la base de datos
    conn = get_db_connection()
    conn.execute(
        'UPDATE creditos SET cliente=?, monto=?, tasa_interes=?, plazo=?, fecha_otorgamiento=? WHERE id=?',
        (cliente, monto, tasa, plazo, fecha, id_)
    )
    conn.commit()
    conn.close()

    flash('Crédito actualizado con éxito.', 'success')
    return redirect('/')

# Ruta para eliminar un crédito
@app.route('/eliminar/<int:id>')
def eliminar_credito(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM creditos WHERE id=?', (id,))
    conn.commit()
    conn.close()

    flash('Crédito eliminado.', 'warning')
    return redirect('/')

# Ruta que devuelve los datos agrupados por cliente para la información que es presentada en la gráfica 
@app.route('/datos')
def datos_creditos():
    conn = get_db_connection()
    datos = conn.execute('SELECT cliente, SUM(monto) as total FROM creditos GROUP BY cliente').fetchall()
    conn.close()
    return jsonify([[row['cliente'], row['total']] for row in datos])

# Inicializa la base de datos y corre la app si se ejecuta directamente
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
