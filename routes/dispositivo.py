from flask import Blueprint
from controllers.dispositivo_controller import *

dispositivo_routes = Blueprint("dispositivo_routes", __name__)

dispositivo_routes.route("/", methods=["POST"])(agregar_dispositivo)
dispositivo_routes.route("/", methods=["GET"])(obtener_dispositivos)
dispositivo_routes.route("/<id>", methods=["GET"])(obtener_dispositivo)
dispositivo_routes.route("/<id>", methods=["PUT"])(actualizar_dispositivo)
dispositivo_routes.route("/<id>", methods=["DELETE"])(eliminar_dispositivo)
dispositivo_routes.route("/import-excel", methods=["POST"])(importar_excel)
dispositivo_routes.route("/export-excel", methods=["GET"])(exportar_excel)
