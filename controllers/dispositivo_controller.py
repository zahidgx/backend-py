from flask import jsonify, request, send_file
from models.dispositivo import DispositivoModel
import pandas as pd
from bson import ObjectId
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from io import BytesIO
from config.database import mongo


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
    try:
        file = request.files['file']
        df = pd.read_excel(file)
        data = df.to_dict(orient="records")

        if data:
            mongo.db.dispositivos.insert_many(data)
            return jsonify({"message": "Datos importados correctamente"}), 201
        else:
            return jsonify({"message": "El archivo está vacío o no tiene datos válidos"}), 400
    except Exception as e:
        return jsonify({"message": f"Error al importar: {str(e)}"}), 500


# Exportar dispositivos a un archivo Excel y enviarlo como respuesta
def exportar_excel():
    try:
        dispositivos = DispositivoModel.obtener_todos_dispositivos()
        if not dispositivos:
            return jsonify({"message": "No hay dispositivos para exportar"}), 400

        df = pd.DataFrame(dispositivos)

        # Convertir el DataFrame en un archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Dispositivos")
            writer.close()

        output.seek(0)

        return send_file(output, download_name="dispositivos_exportados.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return jsonify({"message": f"Error al exportar: {str(e)}"}), 500