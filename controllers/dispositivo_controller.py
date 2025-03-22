from flask import jsonify, request
from models.dispositivo import DispositivoModel
import pandas as pd
from bson import ObjectId

# Agregar un dispositivo
def agregar_dispositivo():
    data = request.json
    DispositivoModel.agregar_dispositivo(data)
    return jsonify({"message": "Dispositivo agregado correctamente"}), 201

# Obtener todos los dispositivos
def obtener_dispositivos():
    dispositivos = DispositivoModel.obtener_todos_dispositivos()  # Llama al método modificado en el modelo
    return jsonify(dispositivos)

# Obtener un dispositivo específico
def obtener_dispositivo(id):
    dispositivo = DispositivoModel.obtener_dispositivo(id)  # Se pasa el id como string
    return jsonify(dispositivo) if dispositivo else jsonify({"message": "Dispositivo no encontrado"}), 404

# Actualizar un dispositivo
def actualizar_dispositivo(id):
    data = request.json
    try:
        result = DispositivoModel.actualizar_dispositivo(id, data)
        
        if result.modified_count > 0:
            return jsonify({"message": "Dispositivo actualizado correctamente"}), 200
        else:
            return jsonify({"message": "No se modificó nada"}), 400
    except Exception as e:
        return jsonify({"message": "Hubo un error al actualizar el dispositivo"}), 500

# Eliminar un dispositivo
def eliminar_dispositivo(id):
    try:
        result = DispositivoModel.eliminar_dispositivo(id)  # Elimina el dispositivo de la colección
        if result.deleted_count > 0:
            return jsonify({"message": "Dispositivo eliminado correctamente"}), 200
        else:
            return jsonify({"message": "Dispositivo no encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Error al eliminar dispositivo"}), 500

# Importar dispositivos desde un archivo Excel
def importar_excel():
    file = request.files['file']
    df = pd.read_excel(file)
    data = df.to_dict(orient="records")
    mongo.db.dispositivos.insert_many(data)  # Ahora usa la colección "dispositivos"
    return jsonify({"message": "Datos importados correctamente"}), 201

# Exportar dispositivos a un archivo Excel
def exportar_excel():
    dispositivos = DispositivoModel.obtener_todos_dispositivos()
    df = pd.DataFrame(dispositivos)
    df.to_excel("dispositivos_exportados.xlsx", index=False)
    return jsonify({"message": "Archivo Excel exportado con éxito"}), 200
