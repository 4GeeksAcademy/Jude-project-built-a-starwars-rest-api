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
from models import db, User, Character, CharacterFavorite, Planet, PlanetFavorite, Vehicle, VehicleFavorite, Starship, StarshipFavorite
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

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': "I can't find this user "}), 400
    return jsonify({'data': user.serialize()}), 200

@app.route('/users/<int:user_id>/favorite', methods=['GET'])
def get_user_favorite(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify({'msg': f'this user id {user_id} not exist'}), 400
    favorite_character_serialize = []
    for favorite in user.favorites:
        favorite_character_serialize.append(favorite.character.serialize())
    
    favorite_planet_serialize = []
    print(favorite_planet_serialize)
    for favorite in user.favorites_planet:
        favorite_planet_serialize.append(favorite.planetas.serialize())

    favorite_vehicle_serialize= []
    for favorite in user.favorite_vehicle:
        favorite_vehicle_serialize.append(favorite.vehiculo.serialize())

    favorite_starship_serialize= []
    for favorite in user.favorite_starship:
        favorite_starship_serialize.append(favorite.starship.serialize())

    return jsonify({'charactere-favorite': favorite_character_serialize,
                    'planet-favorite': favorite_planet_serialize,
                    'vehicle-favorite': favorite_vehicle_serialize,
                    'starship_favorite': favorite_starship_serialize}), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    characters = Character.query.all()
    # print(characters)
    new_serialize= []
    for character in characters:
        new_serialize.append(character.serialize())
    return jsonify({'msg': new_serialize})

@app.route('/people/<int:people_id>', methods= ['GET'])
def get_people_id(people_id):
    character = Character.query.get(people_id)
    if character is None:
        return jsonify({'msg': "I can't find this people"}),400
    return jsonify({'data': character.serialize()}), 200

@app.route('/people', methods= ['POST'])
def add_people():

    body = request.get_json(silent = True)
    if body is None:
        return jsonify({'msg': 'all this fields are required'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'this field cannot be left empty'}), 400
    if 'gender' not in body:
        return jsonify({'msg': 'this field cannot be left empty'}), 400
    if 'birth_day' not in body: 
        return jsonify({'msg': 'this field cannot be left empty'}), 400
    if 'eyes_color' not in body:
        return jsonify({'msg': 'this field cannot be left empty'}), 400
    if 'mass' not in body:
        return jsonify({'msg': 'this field cannot be left empty'}), 400
    if 'height' not in body:
        return jsonify({'msg': 'height is required'})

    new_character = Character()
    # print(new_character)
    new_character.name = body['name']
    new_character.gender= body['gender']
    new_character.birth_day= body['birth_day']
    new_character.eyes_color= body['eyes_color']
    new_character.mass = body['mass']
    new_character.height= body['height']
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'msg': 'your post add successfully'}), 200

@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_people_by_id(people_id, user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'this user not found'}), 404
    
    character = Character.query.get(people_id)
    if character is None:
        return jsonify({'msg': 'character not found'}), 404
    
    favorite_exist = CharacterFavorite.query.filter_by(
        user_id = user_id,
        character_id = people_id
    ).first()
    if favorite_exist:
        return jsonify({'msg': 'this character already existe in favorite'}), 400
    
    new_favorite = CharacterFavorite()

    new_favorite.user_id= user_id,
    new_favorite.character_id = people_id
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'msg': 'charactere added to favorite list'}), 201

@app.route('/people/<int:people_id>', methods=['PUT'])
def edit_character(people_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'body can not be empty'}), 400
    
    character = Character.query.get(people_id)
    if character is None:
        return jsonify({'msg': 'can not find this character'}), 404
    
    if 'name' in body:
        character.name = body['name']
    if 'height' in body:
        character.height = body['height']
    if 'gender' in body:
        character.gender = body['gender']
    if 'eyes_color' in body:
        character.eyes_color = body['eyes_color']
    if 'birth_day' in body:
        character.birth_day = body['birth_day']
    if 'mass' in body:
        character.mass= body['mass']
    db.session.commit()

    return jsonify({'msg': 'character updated succesfully',
                    'data': character.serialize()})

@app.route('/people/<int:people_id>', methods = ['DELETE'])
def delete_people(people_id):
    character  = Character.query.get(people_id)
    if character is None:
        return jsonify({'msg': 'character not found'}), 400
    db.session.delete(character)
    db.session.commit()
    return jsonify({'msg': 'this character delete successfuly'}), 200

# planet

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    new_serialize = []

    for planet in planets:
        new_serialize.append(planet.serialize())
    return jsonify({'data': new_serialize})

@app.route('/planets/<int:planet_id>', methods= ['GET'])
def get_planets_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'this id not exist'})
    return jsonify({'data': planet.serialize()})
           
@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if 'name' not in body:
        return jsonify({'msg': 'name is required in this field'})
    if 'climate' not in body:
        return jsonify({'msg': 'climate is required in this field'})
    if 'diametre' not in body:
        return jsonify({'msg': 'diametre is required in thies field'})
    if 'population' not in body:
        return jsonify({'msg': 'population is required in thies field'})
    
    new_planet = Planet()

    new_planet.name=body['name']
    new_planet.climate = body['climate']
    new_planet.diametre = body['diametre']
    new_planet.population = body['population']
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'planet': new_planet.serialize()})

@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods= ['POST'])
def add_planet_favorite(planet_id, user_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'planet not found'}), 404
    
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'user not found'}), 404
    
    favorite_existe=  PlanetFavorite.query.filter_by(
        user_id = user_id,
        planet_id = planet_id
    ).first()
    if favorite_existe:
        return jsonify({'msg': 'planet already exist in favorit list'}), 400
    
    new_planet_favorite= PlanetFavorite()

    new_planet_favorite.user_id = user_id
    new_planet_favorite.planet_id= planet_id
    db.session.add(new_planet_favorite)
    db.session.commit()

    return jsonify({'msg': 'charactere added to favorite list'}), 200

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def edit_planet(planet_id):
    body=request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'body can not empty'}), 400
    
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'planet not found'}), 404
    
    if 'name' in body:
        planet.name = body['name']
    if 'climate' in body:
        planet.climate = body['climate']
    if 'diametre' in body:
        planet.diametre = body['diametre']
    if 'population' in body:
        planet.population = body['population']
    return jsonify({'planet': planet.serialize()})

@app.route('/planet/<int:planet_id>', methods= ['DELETE'])
def delete_planet(planet_id):
    planet=Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'planot not found'}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'msg': 'planet delete succesfuly'}), 200

# vehicle

@app.route('/vehicles', methods = ['GET'])
def get_all_vehicle():
    vehicles = Vehicle.query.all()
    new_serialize = []

    for vehicle in vehicles:
        new_serialize.append(vehicle.serialize())
    return jsonify({'Vehicle': new_serialize}), 200

@app.route('/vehicle/<int:vehicle_id>', methods = ['GET'])
def get_single_id_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({'msg': 'vehicle not found'}), 404
    return jsonify({'Vehicle': vehicle.serialize()}) 

@app.route('/vehicle', methods = ['POST'])
def add_vehicle():
    body = request.get_json(silent = True)
    if body is None:
        return jsonify({'msg': 'body can not empty'})
    if 'name' not in body:
        return jsonify({'msg': 'name is required'})
    if 'model' not in body:
        return jsonify({'msg': 'model is required'})
    if 'passengers' not in body:
        return jsonify({'msg': 'passengers is requiered'})
    
    new_vehicle = Vehicle()

    new_vehicle.name = body['name']
    new_vehicle.model = body['model']
    new_vehicle.passengers = body['passengers']
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'Vehicle': new_vehicle.serialize()})

@app.route('/favorite/vehicle/<int:vehicle_id>/user/<int:user_id>', methods = ['POST'])
def add_vehicle_favorite(user_id, vehicle_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'user not found'}), 404
    
    vehicle= Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({'msg': 'vehicle not found'}), 404
    
    vehicle_exist = VehicleFavorite.query.filter_by(
        user_id = user_id,
        vehicle_id = vehicle_id
    ). first()
    if vehicle_exist:
        return jsonify({'msg': 'This vehicle is already in favorite'})
    
    new_favorite = VehicleFavorite()
    
    new_favorite.user_id = user_id
    new_favorite.vehicle_id = vehicle_id
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'Favorite planet': 'vehicle add to favorite list'})

@app.route('/vehicle/<int:vehicle_id>', methods = ['PUT'])
def edit_vehicle(vehicle_id):
    body = request.get_json(silent= True)
    if body is None:
        return jsonify({'msg': 'body is requiere'}), 400
    
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({'msg': 'vehicle not found'}), 404
    
    if 'name' in body:
        vehicle.name=body['name']
    if 'model' in body:
        vehicle.model = body['model']
    if 'passengers' in body:
        vehicle.passengers =  body['passengers']
    return jsonify({'vehicle': vehicle.serialize() })

@app.route('/vehicle/<int:vehicle_id>', methods = ['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({'msg': 'vehicle not found'}), 404
    
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'msg': 'this vehicle delete succesfuly'}), 200

# starship

@app.route('/starships', methods = ['GET'])
def get_all_starship():
    starships = Starship.query.all()
    new_serialize = []
    for starship in starships:
        new_serialize.append(starship.serialize())
    return jsonify({'starships': new_serialize}), 200

@app.route('/starship/<int:starship_id>', methods = ['GET'])
def get_ingle_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': 'starship not found'}), 404
    return jsonify({'starship data': starship.serialize()})

@app.route('/starship', methods = ['POST'])
def add_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'body is required'})
    if 'name' not in body:
        return jsonify({'msg': 'This name field is required'}), 400
    if 'model' not in body:
        return jsonify({'msg': 'This model field is required'}), 400
    if 'passengers' not in body:
        return jsonify({'msg': 'This passengers field is required'}), 400
    if 'length' not in body: 
        return jsonify({'msg': 'This length field is required'}), 400
    
    new_starship = Starship()

    new_starship.name= body['name']
    new_starship.model = body['model']
    new_starship.length = body['length']
    new_starship.passengers = body['passengers']

    db.session.add(new_starship)
    db.session.commit()
    return jsonify({'planet': new_starship.serialize()}),201 

@app.route('/favorite/starship/<int:starship_id>/user/<int:user_id>', methods = ['POST'])
def add_favorite(starship_id, user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'msg': 'user not found'}), 404
    
    starship = Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': 'starship not fount'}), 404
    
    starship_exist = StarshipFavorite.query.filter_by(
        user_id = user_id,
        starship_id = starship_id
    ).first()
    if starship_exist:
        return jsonify({'msg': 'starship already exist in favorite'}), 400
    
    new_favorite = StarshipFavorite()

    new_favorite.user_id = user_id
    new_favorite.starship_id = starship_id
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'msg': 'starship add succesfully'}), 201

@app.route('/starship/<int:starship_id>', methods = ['PUT'])
def edit_starship(starship_id):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':' this field body is required'}), 400
    
    starship= Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': 'starship not found'}), 404
    
    if 'name' in body:
        starship.name= body['name']
    if 'model' in body:
        starship.model = body['model']
    if 'passengers' in body:
        starship.passengers = body['passengers']
    if 'length' in body:
        starship.length = body['length']
    db.session.commit()

    return jsonify({'msg': starship.serialize()})

@app.route('/starship/<int:starship_id>', methods = ['DELETE'])
def delete_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        return jsonify({'msg': 'starship not found'}), 404
    db.session.delete(starship)
    db.session.commit()

    return jsonify({'msg': 'starship delete succesfully'}), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
