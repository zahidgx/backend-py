from flask import jsonify, request
from models.alerta import AlertaModel
import pandas as pd
from bson import ObjectId
from config.database import mongo
from flask import send_file
import io

# Agregar una alerta
def agregar_alerta():
    data = request.json
    AlertaModel.agregar_alerta(data)
    return jsonify({"message": "Alerta agregada correctamente"}), 201

# Obtener todas las alertas
def obtener_alertas():
    alertas = AlertaModel.obtener_todas_alertas()  # Llama al método modificado en el modelo
    return jsonify(alertas)

# Obtener una alerta específica
def obtener_alerta(id):
    alerta = AlertaModel.obtener_alerta(ObjectId(id))  # Se pasa el id como ObjectId
    return jsonify(alerta) if alerta else jsonify({"message": "Alerta no encontrada"}), 404

# Actualizar una alerta
def actualizar_alerta(id):
    data = request.json
    try:
        result = AlertaModel.actualizar_alerta(ObjectId(id), data)
        
        if result.modified_count > 0:
            return jsonify({"message": "Alerta actualizada correctamente"}), 200
        else:
            return jsonify({"message": "No se modificó nada"}), 400
    except Exception as e:
        return jsonify({"message": "Hubo un error al actualizar la alerta"}), 500

# Eliminar una alerta
def eliminar_alerta(id):
    try:
        result = AlertaModel.eliminar_alerta(ObjectId(id))  # Elimina la alerta de la colección
        if result.deleted_count > 0:
            return jsonify({"message": "Alerta eliminada correctamente"}), 200
        else:
            return jsonify({"message": "Alerta no encontrada"}), 404
    except Exception as e:
        return jsonify({"message": "Error al eliminar alerta"}), 500

# Importar alertas desde un archivo Excel
def importar_excel():
    file = request.files['file']
    df = pd.read_excel(file)
    data = df.to_dict(orient="records")
    mongo.db.alertas.insert_many(data)  # Ahora usa la colección "alertas"
    return jsonify({"message": "Datos importados correctamente"}), 201

# Exportar alertas y permitir descarga desde la página web
def exportar_excel():
    alertas = list(mongo.db.alertas.find({}, {"_id": 0}))  # Excluir _id
    df = pd.DataFrame(alertas)  # Convertir a DataFrame
    
    output = io.BytesIO()  # Crear buffer en memoria
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Alertas")

    output.seek(0)  # Volver al inicio del archivo
    return send_file(output, download_name="alertas.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
