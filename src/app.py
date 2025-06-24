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
from models import db, User, Characters, Planets, User_Planet, User_Character
# from models import Classes

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


def character_to_dict(self):
    return {
        id: self.id,
        'name': self.name,
        'eye_color': self.eye_color,
        'hair_color': self.hair_color,
        'height': self.height,

    }


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def handle_all_users():

    response_body = {
        "msg": "return all the users in the db "
    }

    return jsonify(response_body), 200


@app.route('/users/favorites/planets', methods=['GET'])
def get_all_user_favorite_planets():
    user_favorites = User_Planet.query.get_404()
    if user_favorites:
        return jsonify(user_favorites), 200


@app.route('/users/favorites/people', methods=['GET'])
def get_all_user_favorite_people():
    user_favorite_people = User_Character.query.get_404()
    if user_favorite_people:
        return jsonify(user_favorite_people), 200


@app.route('/people', methods=['GET'])
def get_all_people():
    people = Characters.query.all()
    return jsonify([people.character_to_dict()] for character in Characters)

    # make query to the people(character)table and get all the people
    # return the people from the db
    # return jsonify({"msg": "all people from the DB"})


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person():
    # connect to the db
    # query for the person_id
    # return the single person with that person_id
    return jsonify({"msg": "Here is the person with person_id"})


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
# def add_new_favorite_planet():
# Build this
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
# def add_new_favorite_people():
# Build this
@app.route('/planets', methods=['GET'])
def get_all_planets():
    # make connection to the db
    # search for all the Planets
    # return all the planets
    return jsonify({"msg": "all planets from the DB"})


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_a_planet_by_id():
    # find_planet_id =

    # DELETE FAV PLANET BY ID


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    # connect to the db
    planet = Planets.query.get_or_404(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted successfully"}), 204
    else:
        return jsonify({"error": "planet not found"}), 404

# DELETE USER Fav People by id


@app.route('[DELETE] /favorite/people/<int:people_id>', methods=['DELETE'])
def delete_user_person_fav(fav_id):

    fav_planet = User_Character.query.get_or_404(fav_id)
    if fav_planet:
        db.session.delete(fav_planet)
        db.session.commit()
        return jsonify({"message": "Fav Planet deleted successfully"}), 204
    else:
        return jsonify({"error": "Fav planet not found"}), 404


# Keep At the Bottom of the File
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
