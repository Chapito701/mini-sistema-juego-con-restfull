from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import controlador_juegos

# Creamos un Blueprint para agrupar todas las rutas de la API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class JuegoList(Resource):
    """
    Endpoint para obtener todos los juegos o crear uno nuevo.
    Ruta: /api/juegos
    """
    def get(self):
        # GET /api/juegos: Obtiene la lista de juegos
        juegos_tuplas = controlador_juegos.obtener_juegos()
        
        # Serialización de objetos (tuplas a diccionarios para JSON)
        juegos_json = []
        for j in juegos_tuplas:
            juegos_json.append({
                "id": j[0],
                "nombre": j[1],
                "descripcion": j[2],
                "precio": float(j[3]) if j[3] is not None else 0.0
            })
        return juegos_json, 200

    def post(self):
        # POST /api/juegos: Crea un nuevo juego
        datos = request.get_json()
        
        # Validación de peticiones inválidas (400 Bad Request)
        if not datos or not 'nombre' in datos or not 'descripcion' in datos or not 'precio' in datos:
            return {"mensaje": "Faltan datos requeridos (nombre, descripcion, precio)"}, 400
        
        try:
            controlador_juegos.insertar_juego(datos['nombre'], datos['descripcion'], datos['precio'])
            return {"mensaje": "Juego creado exitosamente"}, 201 # 201 Created
        except Exception as e:
            return {"mensaje": str(e)}, 500


class JuegoResource(Resource):
    """
    Endpoint para obtener, actualizar o eliminar un juego específico por su ID.
    Ruta: /api/juegos/<int:id>
    """
    def get(self, id):
        # GET /api/juegos/<id>
        juego = controlador_juegos.obtener_juego_por_id(id)
        
        # Verificar código de error 404 Not Found
        if juego is None:
            return {"mensaje": "Juego no encontrado"}, 404
        
        # Serialización
        juego_json = {
            "id": juego[0],
            "nombre": juego[1],
            "descripcion": juego[2],
            "precio": float(juego[3]) if juego[3] is not None else 0.0
        }
        return juego_json, 200

    def put(self, id):
        # PUT /api/juegos/<id>: Modificar un juego existente
        juego = controlador_juegos.obtener_juego_por_id(id)
        if juego is None:
            return {"mensaje": "Juego no encontrado"}, 404

        datos = request.get_json()
        if not datos or not 'nombre' in datos or not 'descripcion' in datos or not 'precio' in datos:
            return {"mensaje": "Faltan datos requeridos (nombre, descripcion, precio)"}, 400
        
        try:
            controlador_juegos.actualizar_juego(datos['nombre'], datos['descripcion'], datos['precio'], id)
            return {"mensaje": "Juego actualizado exitosamente"}, 200
        except Exception as e:
            return {"mensaje": str(e)}, 500

    def delete(self, id):
        # DELETE /api/juegos/<id>: Eliminar un juego
        juego = controlador_juegos.obtener_juego_por_id(id)
        if juego is None:
            return {"mensaje": "Juego no encontrado"}, 404

        try:
            controlador_juegos.eliminar_juego(id)
            return '', 204 # 204 No Content (petición exitosa, sin cuerpo de respuesta)
        except Exception as e:
            return {"mensaje": str(e)}, 500

# Definición de los recursos y sus URLs en Flask-RESTful
api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')