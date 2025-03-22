from flask import Blueprint
from controllers.usuario_controller import *

usuario_routes = Blueprint("usuario_routes", __name__)

# Rutas de usuario
usuario_routes.route("/", methods=["POST"])(agregar_usuario)
usuario_routes.route("/", methods=["GET"])(obtener_usuarios)
usuario_routes.route("/<id>", methods=["GET"])(obtener_usuario)
usuario_routes.route("/<id>", methods=["PUT"])(actualizar_usuario)
usuario_routes.route("/<id>", methods=["DELETE"])(eliminar_usuario)  # Ruta para eliminar un usuario
usuario_routes.route("/import-excel", methods=["POST"])(importar_excel)
usuario_routes.route("/export-excel", methods=["GET"])(exportar_excel)
