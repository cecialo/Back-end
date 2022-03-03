


from flask import Flask,jsonify,request
#from flask_pymongo import PyMongo
from flask_cors import CORS
import json
from bson import json_util

app=Flask(__name__)
CORS(app)

import pymongo

#todo creo el objeto para conectarme con Mongodb
database=pymongo.MongoClient()
#todo me conecto con el servidor local
database =pymongo.MongoClient("mongodb://localhost:27017/")
#todo me conecto a la bd cargamos y a la coleccion alumnos
alumnos = database["cargamos"]["alumnos"]

# todo crear un servicio que retorne todos los documentos de 
# todo mi coleccion alumnos

@app.route('/api/alumnos' ,methods=['GET'])
def mostrar_alumnos():
    lista_alumnos =[]
    for docu in alumnos.find():
        lista_alumnos.append(docu)
        
    return json.dumps(lista_alumnos,default=json_util.default)    

@app.route('/api/register',methods=['POST'])
def register():
    
    #todo en que formato insertare los valores
    data=request.get_json()
    
    obj = {
        "name" : data["name"],
        "apellido" : data["apellido"],
        "edad":data["edad"]
    }
    
    res=alumnos.insert_one(obj)
    
    return jsonify({
        "message" : "alumnos registrado correctamente",
        "status":200
    })
        
@app.route('/api/alumnos/<name>' ,methods=['GET'])
def mostrar_alumno(name):
    alumno=alumnos.find_one({"name":name})
    return json.dumps(alumno,default=json_util.default)    


@app.route('/api/delete/<name>',methods=['DELETE'])
def remove(name):
    alumnos.delete_one({"name": name})    
    return jsonify ({
        "message" : "{} eliminado ".format(name)
    })
    
@app.route('/api/update/<name>',methods =["PUT"])
def update(name):
    #todo nuevo valor que tomara el nombre
    data = request.get_json()
    #todo el valor actual que voy a actulizar
    query = {"name":name,
            }
    
    alumnos.update_one(query, {"$set":data})   
    
    return jsonify ({
        "message" :"{} actualizado" .format(name)
    })
    
    
app.run(debug=True,port=5000)
