from flask import jsonify, request, send_file
from models.usuario import UsuarioModel
import pandas as pd
from bson import ObjectId
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from io import BytesIO
from config.database import mongo  # Importar la conexión a la base de datos

# Agregar un usuario
def agregar_usuario():
    data = request.json
    UsuarioModel.agregar_usuario(data)
    return jsonify({"message": "Usuario agregado correctamente"}), 201

# Obtener todos los usuarios
def obtener_usuarios():
    usuarios = UsuarioModel.obtener_todos_usuarios()
    return jsonify(usuarios)

# Obtener un usuario específico
def obtener_usuario(id):
    usuario = UsuarioModel.obtener_usuario(id)
    return jsonify(usuario) if usuario else jsonify({"message": "Usuario no encontrado"}), 404

# Actualizar un usuario
def actualizar_usuario(id):
    data = request.json
    try:
        result = UsuarioModel.actualizar_usuario(id, data)
        if result.modified_count > 0:
            return jsonify({"message": "Usuario actualizado correctamente"}), 200
        else:
            return jsonify({"message": "No se modificó nada"}), 400
    except Exception as e:
        return jsonify({"message": f"Hubo un error al actualizar el usuario: {e}"}), 500

# Eliminar un usuario
def eliminar_usuario(id):
    try:
        result = UsuarioModel.eliminar_usuario(id)
        if result.deleted_count > 0:
            return jsonify({"message": "Usuario eliminado correctamente"}), 200
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": f"Error al eliminar usuario: {e}"}), 500

# Importar usuarios desde un archivo Excel
def importar_excel():
    if 'file' not in request.files:
        return jsonify({"error": "No se ha enviado un archivo"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400
    
    filename = secure_filename(file.filename)
    
    # Leer el archivo Excel
    df = pd.read_excel(file)
    if "email" not in df.columns:
        return jsonify({"error": "El archivo debe contener una columna 'email'"}), 400

    nuevos_usuarios = []
    for _, row in df.iterrows():
        email = row.get("email")
        if email and not mongo.db.users.find_one({"email": email}):  # Corregido
            nuevos_usuarios.append({
                "nombre": row.get("nombre", ""),
                "apellido_paterno": row.get("apellido_paterno", ""),
                "apellido_materno": row.get("apellido_materno", ""),
                "email": email,
                "password": row.get("password", ""),
                "fechaNacimiento": row.get("fechaNacimiento", ""),
                "rol": row.get("rol", "usuario"),
                "foto_perfil": row.get("foto_perfil", ""),
                "intentos": row.get("intentos", 0),
                "bloqueo_hasta": row.get("bloqueo_hasta", None)
            })
    
    if nuevos_usuarios:
        mongo.db.users.insert_many(nuevos_usuarios)  # Corregido

    return jsonify({"message": f"{len(nuevos_usuarios)} usuarios importados correctamente"}), 201

# Exportar usuarios a un archivo Excel
def exportar_excel():
    usuarios = list(mongo.db.users.find({}, {"_id": 0}))  # Corregido
    
    if not usuarios:
        return jsonify({"error": "No hay usuarios para exportar"}), 400

    df = pd.DataFrame(usuarios)
    
    # Guardar en un buffer en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Usuarios')

    output.seek(0)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True, download_name="usuarios.xlsx")
