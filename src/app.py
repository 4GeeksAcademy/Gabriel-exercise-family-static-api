"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        return jsonify(jackson_family.get_all_members()), 200
    except:
        return jsonify({"Error": "Server Error"}), 500

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        return jsonify(jackson_family.get_member(id)), 200
    except:
        return jsonify({"Error": "Server Error"}), 500

@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.get_json()

        if not data.get('first_name') or not data.get('age') or not data.get('lucky_numbers'):
            return jsonify({"Error": "valor introducido no válido"}), 400

        jackson_family.add_member(data)
        return jsonify({"message": "Member added successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error"}), 500


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        jackson_family.delete_member(id)
        return jsonify({"message": "Member deleted successfully"}), 200
    except:
        return jsonify({"error": "Server error"}), 500

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()

        # Verificar si los datos requeridos están presentes
        if not data.get("first_name") or not data.get("age") or not isinstance(data.get("lucky_numbers"), list):
            return jsonify({"error": "Invalid request, missing fields"}), 400

        # Obtener el miembro a actualizar
        member = jackson_family.get_member(member_id)

        if not member:
            return jsonify({"error": "Member not found"}), 404

        # Actualizar los campos del miembro
        member["first_name"] = data["first_name"]
        member["age"] = data["age"]
        member["lucky_numbers"] = data["lucky_numbers"]

        return jsonify({"message": "Member updated successfully"}), 200
    except:
        return jsonify({"error": "Server error"}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

