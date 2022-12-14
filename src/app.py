"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():

    members = jackson_family.get_all_members()
    response_body = {

        "family": members
    }

    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    response_body = {

        "family": member
    }
    return jsonify(member), 200


@app.route('/member>', methods=['POST'])
def add_new_member():

    # this is how you can use the Family datastructure by calling its methods

    body_name = request.json.get("first_name")
    body_age = request.json.get("age")
    body_id = request.json.get("id")
    body_lucky_numbers = request.json.get("lucky_numbers")

    member = {
        "id": body_id or jackson_family._generateId(),
        "first_name": body_name,
        "age": body_age,
        "lucky_numbers": body_lucky_numbers
    }

    members = jackson_family.add_member(member)

    return jsonify("A new family member is born"), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    members = jackson_family.delete_member(member_id)

    return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
