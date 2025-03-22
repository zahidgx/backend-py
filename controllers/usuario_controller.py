from flask import jsonify, request
from models.usuario import UsuarioModel
import pandas as pd
from bson import ObjectId

# Agregar un usuario
def agregar_usuario():
    data = request.json
    UsuarioModel.agregar_usuario(data)
    return jsonify({"message": "Usuario agregado correctamente"}), 201

# Obtener todos los usuarios
def obtener_usuarios():
    usuarios = UsuarioModel.obtener_todos_usuarios()  # Llama al método modificado en el modelo
    return jsonify(usuarios)

# Obtener un usuario específico
def obtener_usuario(id):
    usuario = UsuarioModel.obtener_usuario(id)  # Se pasa el id como string
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
        return jsonify({"message": "Hubo un error al guardar el usuario"}), 500

# Eliminar un usuario
def eliminar_usuario(id):
    try:
        result = UsuarioModel.eliminar_usuario(id)  # Elimina el usuario de la colección
        if result.deleted_count > 0:
            return jsonify({"message": "Usuario eliminado correctamente"}), 200
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Error al eliminar usuario"}), 500

# Importar usuarios desde un archivo Excel
def importar_excel():
    file = request.files['file']
    df = pd.read_excel(file)
    data = df.to_dict(orient="records")
    mongo.db.users.insert_many(data)
    return jsonify({"message": "Datos importados correctamente"}), 201

# Exportar usuarios a un archivo Excel
def exportar_excel():
    usuarios = UsuarioModel.obtener_todos_usuarios()
    df = pd.DataFrame(usuarios)
    df.to_excel("users_exportados.xlsx", index=False)
    return jsonify({"message": "Archivo Excel exportado con éxito"}), 200
