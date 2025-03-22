from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
import smtplib
from email.mime.text import MIMEText
from config.database import mongo

auth_routes = Blueprint('auth', __name__)

SECRET_KEY = "tu_secreto"

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    if mongo.db.users.find_one({"email": data['email']}):
        return jsonify({"msg": "Usuario ya registrado"}), 400

    hashed_password = generate_password_hash(data['password'])
    nuevo_usuario = {
        "nombre": data['nombre'],
        "apellido_paterno": data['apellido_paterno'],
        "apellido_materno": data['apellido_materno'],
        "email": data['email'],
        "password": hashed_password,
        "fechaNacimiento": data['fechaNacimiento'],
        "rol": "usuario",
        "intentos": 0,
        "bloqueo_hasta": None
    }

    mongo.db.users.insert_one(nuevo_usuario)
    return jsonify({"msg": "Usuario registrado exitosamente"}), 201


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({"email": data['email']})

    if not user:
        return jsonify({"msg": "Credenciales incorrectas"}), 400

    # Verificar si la cuenta está bloqueada
    if user.get("bloqueo_hasta") and datetime.datetime.utcnow() < user["bloqueo_hasta"]:
        return jsonify({"msg": f"Cuenta bloqueada hasta {user['bloqueo_hasta']}"}), 403

    if not check_password_hash(user["password"], data["password"]):
        user["intentos"] = user.get("intentos", 0) + 1

        # Bloquear la cuenta si falla 3 veces
        if user["intentos"] >= 3:
            user["bloqueo_hasta"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
            mongo.db.users.update_one({"email": data['email']}, {"$set": user})
            return jsonify({"msg": "Cuenta bloqueada por 3 minutos"}), 403

        mongo.db.users.update_one({"email": data['email']}, {"$set": {"intentos": user["intentos"]}})
        return jsonify({"msg": "Credenciales incorrectas"}), 400

    # Restablecer intentos si inicia sesión correctamente
    mongo.db.users.update_one({"email": data['email']}, {"$set": {"intentos": 0, "bloqueo_hasta": None}})

    token = jwt.encode({"user_id": str(user["_id"]), "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "user": {k: v for k, v in user.items() if k != "password"}})


@auth_routes.route('/usuario/<email>', methods=['GET'])
def buscar_usuario(email):
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    return jsonify({"user": {k: v for k, v in user.items() if k != "password"}})


@auth_routes.route('/recuperar-password', methods=['POST'])
def recuperar_password():
    data = request.json
    user = mongo.db.users.find_one({"email": data["email"]})

    if not user:
        return jsonify({"msg": "No se encontró un usuario con este email"}), 400

    token = jwt.encode({"user_id": str(user["_id"]), "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, SECRET_KEY, algorithm="HS256")

    msg = MIMEText(f"Haz clic en el siguiente enlace para restablecer tu contraseña:\n http://localhost:5173/reset-password/{token}")
    msg["Subject"] = "Recuperación de contraseña"
    msg["From"] = "tu_correo@gmail.com"
    msg["To"] = user["email"]

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("tu_correo@gmail.com", "tu_contraseña")
        server.sendmail("tu_correo@gmail.com", user["email"], msg.as_string())
        server.quit()
        return jsonify({"msg": "Se ha enviado un correo con instrucciones"}), 200
    except Exception as e:
        return jsonify({"msg": "Error enviando el correo", "error": str(e)}), 500


@auth_routes.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    try:
        decoded = jwt.decode(data["token"], SECRET_KEY, algorithms=["HS256"])
        user = mongo.db.users.find_one({"_id": decoded["user_id"]})

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 400

        hashed_password = generate_password_hash(data["password"])
        mongo.db.users.update_one({"_id": decoded["user_id"]}, {"$set": {"password": hashed_password}})
        return jsonify({"msg": "Contraseña restablecida con éxito"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "El token ha expirado"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Token inválido"}), 400
