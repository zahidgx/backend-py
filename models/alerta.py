from bson import ObjectId
from config.database import mongo

class AlertaModel:
    @staticmethod
    def agregar_alerta(data):
        return mongo.db.alertas.insert_one(data)

    @staticmethod
    def obtener_todas_alertas():
        alertas = mongo.db.alertas.find()  # No excluir el _id
        alertas_lista = list(alertas)
        
        # Convertir _id a string antes de devolver
        for alerta in alertas_lista:
            alerta["_id"] = str(alerta["_id"])  # Convertir el _id de ObjectId a string
        
        return alertas_lista

    @staticmethod
    def obtener_alerta(id):
        alerta = mongo.db.alertas.find_one({"_id": ObjectId(id)})
        if alerta:
            alerta["_id"] = str(alerta["_id"])  # Convertir _id a string
        return alerta

    @staticmethod
    def actualizar_alerta(id, data):
        try:
            object_id = ObjectId(id)  # Asegúrate de que el ID sea un ObjectId
            result = mongo.db.alertas.update_one({"_id": object_id}, {"$set": data})
            return result
        except Exception as e:
            print(f"Error al actualizar alerta: {e}")
            return None

    @staticmethod
    def eliminar_alerta(id):
        object_id = ObjectId(id)
        return mongo.db.alertas.delete_one({"_id": object_id})

    def save(self):
        mongo.db.alertas.insert_one(self.__dict__)

    @staticmethod
    def find_by_name(name):
        return mongo.db.alertas.find_one({"name": name})

    def update(self):
        mongo.db.alertas.update_one({"name": self.name}, {"$set": self.__dict__})
