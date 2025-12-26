"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_user():
    users = User.query.all()
    new_serialize = []
    for user in users:
        new_serialize.append(user.serialize())
    return jsonify({'data': new_serialize}), 200

@app.route('/users', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Body can not empty'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'this field cannot be left empty'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'Enter the password before you continue'}), 400
    if 'is_active' not in body:
        return jsonify({'msg': 'is_active is required'}), 400

    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = body['is_active']
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "your post add successfully"}), 201

@app.route('/users/<int:user_id>', methods=['Get'])
def get_user_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': "I can't find this user "}), 404
    return jsonify({'data': user.serialize()})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
