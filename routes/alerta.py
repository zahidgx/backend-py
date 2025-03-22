from flask import Blueprint
from controllers.alerta_controller import *

alerta_routes = Blueprint("alerta_routes", __name__)

alerta_routes.route("/", methods=["POST"])(agregar_alerta)
alerta_routes.route("/", methods=["GET"])(obtener_alertas)
alerta_routes.route("/<id>", methods=["GET"])(obtener_alerta)
alerta_routes.route("/<id>", methods=["PUT"])(actualizar_alerta)
alerta_routes.route("/<id>", methods=["DELETE"])(eliminar_alerta)
alerta_routes.route("/import-excel", methods=["POST"])(importar_excel)
alerta_routes.route("/export-excel", methods=["GET"])(exportar_excel)
