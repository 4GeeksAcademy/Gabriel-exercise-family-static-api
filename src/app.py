"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({'id':3443, 'first_name': 'Tommy', 'age':33, 'lucky_numbers':[7, 13, 22]})
jackson_family.add_member({'first_name': 'Jane', 'age': 35, 'lucky_numbers':[10, 14, 3]})
jackson_family.add_member({'first_name': 'Jimmy', 'age':5, 'lucky_numbers': [1]})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()


    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({'msg': f'El miembro con el id:{id} no existe'}),404
    else:
        return jsonify(member),200
    
@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    if 'first_name' not in data or 'age' not in data or 'lucky_numbers' not in data:
        return jsonify({"msg": "faltan parametros en la soliciutd"}), 400
    else:
        jackson_family.add_member(data)
        return jsonify({'msg': 'miembor añadido', 'member': data}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({'done': True}), 200
    else:
        return jsonify({'msg': 'miembro no encontrado'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
