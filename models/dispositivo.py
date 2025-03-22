from bson import ObjectId
from config.database import mongo

class DispositivoModel:
    @staticmethod
    def agregar_dispositivo(data):
        return mongo.db.dispositivos.insert_one(data)

    @staticmethod
    def obtener_todos_dispositivos():
        dispositivos = mongo.db.dispositivos.find()  # No excluir el _id
        dispositivos_lista = list(dispositivos)
        
        # Convertir _id a string antes de devolver
        for dispositivo in dispositivos_lista:
            dispositivo["_id"] = str(dispositivo["_id"])  # Convertir el _id de ObjectId a string
        
        return dispositivos_lista

    @staticmethod
    def obtener_dispositivo(id):
        dispositivo = mongo.db.dispositivos.find_one({"_id": ObjectId(id)})
        if dispositivo:
            dispositivo["_id"] = str(dispositivo["_id"])  # Convertir _id a string
        return dispositivo

    @staticmethod
    def actualizar_dispositivo(id, data):
        try:
            object_id = ObjectId(id)  # Asegúrate de que el ID sea un ObjectId
            result = mongo.db.dispositivos.update_one({"_id": object_id}, {"$set": data})
            return result
        except Exception as e:
            print(f"Error al actualizar dispositivo: {e}")
            return None

    @staticmethod
    def eliminar_dispositivo(id):
        object_id = ObjectId(id)
        return mongo.db.dispositivos.delete_one({"_id": object_id})

    def save(self):
        mongo.db.dispositivos.insert_one(self.__dict__)

    @staticmethod
    def find_by_name(name):
        return mongo.db.dispositivos.find_one({"name": name})

    def update(self):
        mongo.db.dispositivos.update_one({"name": self.name}, {"$set": self.__dict__})
