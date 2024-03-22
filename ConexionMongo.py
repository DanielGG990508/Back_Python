from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configura la conexión a MongoDB
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/Themis"
mongo = PyMongo(app)


@app.route('/Pruebas')

@app.route('/Pruebas/Conection')
def get_connection():  # Función renombrada a 'get_connection' para cumplir con convenciones
    print("<< Entro al servicio >>")
    return "¡Hola mundo conexión!"  # Mensaje de respuesta

@app.route('/Pruebas/Insertar',methods=['POST'])
def insertar_empleado():
    try:
        data = request.json.get("data")
        empleado_id = mongo.db.Empleado.insert_one(data).inserted_id
        return jsonify({"Empleado Insertado": str(empleado_id)})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/Pruebas/Listar',methods=['GET'])
def consultaGeneral():
    empleados = list(mongo.db.Empleado.find({}))
    if empleados:
        return jsonify({"data": empleados})
    else:
        return jsonify({"message": "Empleado no encontrado"})

@app.route('/Pruebas/Eliminar', methods=['DELETE'])
def eliminar_empleado():
    try:
        empleado_id=request.json.get("_id")
        result = mongo.db.Empleado.delete_one({"_id":empleado_id})
        if result.deleted_count > 0:
            return jsonify({"message": "Empleado eliminado correctamente"})
        else:
            return jsonify({"message": "Empleado no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/Pruebas/Empleado',methods=['GET'])
def consultaEmpleado():
    empleado_id=request.json.get("_id")
    empleados = list(mongo.db.Empleado.find({"_id": empleado_id}))
    if empleados:
        for empleado in empleados:
            empleado["_id"] = str(empleado["_id"])
        return jsonify({"message": "Empleado encontrado", "data": empleado})
    else:
        return jsonify({"message": "Empleado no encontrado"})

@app.route('/Pruebas/Editar', methods=['PUT'])
def editar_empleado(empleado_id):
    try:
        data = request.json
        result = mongo.db.Empleado.update_one({"_id": empleado_id}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Empleado actualizado correctamente"})
        else:
            return jsonify({"message": "Empleado no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Arranque de la aplicación:
if __name__ == '__main__':
    app.run(debug=True)  # Activa modo desarrollo para facilitar la corrección de errores
