from bson import ObjectId
from config.database import mongo

class UsuarioModel:
    @staticmethod
    def agregar_usuario(data):
        return mongo.db.users.insert_one(data)

    @staticmethod
    def obtener_todos_usuarios():
        usuarios = mongo.db.users.find()  # No excluir el _id
        usuarios_lista = list(usuarios)
        
        # Convertir _id a string antes de devolver
        for usuario in usuarios_lista:
            usuario["_id"] = str(usuario["_id"])  # Convertir el _id de ObjectId a string
        
        return usuarios_lista

    @staticmethod
    def obtener_usuario(id):
        usuario = mongo.db.users.find_one({"_id": ObjectId(id)})
        if usuario:
            usuario["_id"] = str(usuario["_id"])  # Convertir _id a string
        return usuario

    @staticmethod
    def actualizar_usuario(id, data):
        try:
            object_id = ObjectId(id)  # Asegúrate de que el ID sea un ObjectId
            result = mongo.db.users.update_one({"_id": object_id}, {"$set": data})
            return result
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return None

    @staticmethod
    def eliminar_usuario(id):
        object_id = ObjectId(id)
        return mongo.db.users.delete_one({"_id": object_id})

    def save(self):
        mongo.db.users.insert_one(self.__dict__)

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    def update(self):
        mongo.db.users.update_one({"email": self.email}, {"$set": self.__dict__})
