from flask import Flask, render_template, request, redirect, url_for, flash
import os
import psycopg2

#RUTA ABSOLUTA A LA CARPETA DE TEMPLATES
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.secret_key = "clave_segura"

# DATOS DE CONEXIÓN A BASE DE DATOS
DB_HOST = "localhost"
DB_NAME = "Formulario_db"
DB_USER = "postgres"
DB_PASS = "123456"
def get_db_connection():
    """Función para conectarse a la base de datos PostgreSQL"""
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# =====================================
# RUTA PRINCIPAL (MUESTRA EL FORMULARIO)
# =====================================

@app.route("/", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO public."Contactos" ("Nombre", "Apellido", "Direccion", "Telefono", "Correo", "Mensaje")
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, direccion, telefono, correo, mensaje))
            conn.commit()
            cur.close()
            conn.close()

            flash(" Registro guardado correctamente.", "success")
            return redirect(url_for("success"))
        except Exception as e:
            flash(f" Error al guardar: {e}", "danger")

    return render_template("form.html")

# =====================================
# RUTA DE CONFIRMACIÓN (PÁGINA SUCCESS)
# =====================================

@app.route("/success")
def success():
    return render_template("success.html")

# =====================================
# EJECUTAR FLASK
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
