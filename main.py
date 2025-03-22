from flask import Flask
from flask_cors import CORS
from routes.alerta import alerta_routes
from config.database import mongo
from routes.dispositivo import dispositivo_routes
from routes.usuario import usuario_routes
from routes.auth import auth_routes

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend

# Configuración de MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/SoundAlertIA"
mongo.init_app(app)

# Registrar las rutas de alertas
app.register_blueprint(alerta_routes, url_prefix="/api/alertas")

app.register_blueprint(dispositivo_routes, url_prefix="/api/dispositivos")

app.register_blueprint(usuario_routes, url_prefix="/api/usuarios")

app.register_blueprint(auth_routes, url_prefix="/api/auth")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
