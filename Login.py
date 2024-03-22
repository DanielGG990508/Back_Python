import os
import time
import binascii
from Segurity import Security
from dotenv import load_dotenv
from Crypto.PublicKey import RSA
from flask_pymongo import PyMongo
from Crypto.Cipher import PKCS1_OAEP
from flask import Flask, jsonify, request

#Acceso a las variables de entorno
load_dotenv()
privateKey=RSA.import_key(binascii.unhexlify(os.getenv('privateKey')))
publicKey=RSA.import_key(binascii.unhexlify(os.getenv('publicKey')))
cipher=PKCS1_OAEP.new(privateKey)
secreto=os.getenv('secreto')

time=int(time.time())

#declaracion de la APP
app = Flask(__name__)

# Configura la conexión a MongoDB
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/Themis"
mongo = PyMongo(app)

#Servicios Web
@app.route('/Login')

@app.route('/Login/Conection')
def get_connection():
    print("<< Entro al servicio >>")
    return "¡Hola mundo conexión!"

@app.route('/Login/Insertar',methods=['POST'])
def insertar_Usuario():
    try:
        data = request.json.get("data")
        # usuario=cipher.encrypt(data.get("Usuario").encode())
        # contraseña=cipher.encrypt(data.get("Contraseña").encode())
        # data={"Usuario":usuario, "Contraseña":contraseña,"_id":data.get("_id")}
        usuario_id = mongo.db.Usuarios.insert_one(data).inserted_id
        return jsonify({"Usuario Insertado":usuario_id})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/Login/Eliminar', methods=['DELETE'])
def eliminar_Usuario():
    try:
        usurio_id=request.json.get("_id")
        result = mongo.db.Usuarios.delete_one({"_id":usurio_id})
        if result.deleted_count > 0:
            return jsonify({"message": "Usuario eliminado correctamente"})
        else:
            return jsonify({"message": "Usuario no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/Login/Editar', methods=['PUT'])
def editar_Usuario(usuario_id):
    try:
        data = request.json
        result = mongo.db.Usuarios.update_one({"_id": usuario_id}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Usuario actualizado correctamente"})
        else:
            return jsonify({"message": "Usuario no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/Login/Usuario',methods=['GET'])
def consultaUsuario():
    usuario_id=request.json.get("_id")
    usuarios = list(mongo.db.Usuarios.find({"_id": usuario_id}))
    if usuarios:
        for usuario in usuarios:
            usuario["_id"] = str(usuario["_id"])
        return jsonify({"message": "Usuario encontrado", "data": usuario})
    else:
        return jsonify({"message": "Usuario no encontrado"})

@app.route('/Login/Listar',methods=['GET'])
def consultaGeneral():
    acceso=Security.verify_token(request.headers)
    print(acceso[0])
    if acceso and acceso == 'Dependiente':
        try:
            usuarios = list(mongo.db.Usuarios.find({}))
            if usuarios:
                return jsonify({"data": usuarios})
            else:
                return jsonify({"message": "Usuario no encontrado"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"mensaje":"Usuario no autorizado"}),401

@app.route('/Login/Inicio',methods=['GET'])
def Inicio_Sesion():
    try:
        # usuario=cipher.decrypt(request.json.get("Usuario"))
        usuario=request.json.get("Usuario")
        print("<<Usuario>>",usuario)
        # contreseña=cipher.decrypt(request.json.get("Contreseña"))
        contreseña=request.json.get("Contreseña")
        print("<<Contraseña>>",contreseña)
        usuarioBD = mongo.db.Usuarios.find_one({"Usuario":usuario})
        if usuarioBD:
            if contreseña==usuarioBD.get("Contraseña"):
                userToken=Security.generate_token(usuario,usuarioBD.get("Perfil"))
                return jsonify (f"Inicio correcto",{"token":userToken})
            else:
                return jsonify (f"Contraseña incorrecta")
        else:
            return jsonify (f"El usuario {usuario} no existe")
    except Exception as e:
        return jsonify({"error": str(e)})

# Arranque de la aplicación:
if __name__ == '__main__':
    app.run(debug=True)