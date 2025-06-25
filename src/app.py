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
from models import db, User, Characters, Planets, Favorites
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


@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = Characters.query.all()
    return jsonify([person.serialize() for person in all_people])


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = Characters.query.get_or_404(people_id)
    return jsonify(person.serialize())


@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in all_planets])


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    return jsonify(planet.serialize())


@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    return jsonify([user.serialize() for user in all_users])


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_favorites(user_id):
    current_user = User.query.get_or_404(user_id)
    favorites = Favorites.query.filter_by(user_id == current_user.id).all()
    return jsonify([favorite.serialize() for favorite in favorites])


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    user = User.query.first()
    new_favorite = Favorites(user_id=user.id, planet_id=planet.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "New Favorite planet Added"})


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    person = Characters.query.get_or_404(people_id)
    user = User.query.first()
    new_favorite = Favorites(user_id=user.id, people_id=person.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "New Favorite Character Added"})


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    user = User.query.first()
    result = db.session.query(Favorites).filter_by(
        user_id=user.id, planet_id=planet_id).delete()
    if result > 0:
        db.session.commit()
    return jsonify({"message": "Favorite Planet deleted"})


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_person(people_id):
    user = User.query.first()
    result = db.session.query(Favorites).filter_by(
        user_id=user.id, ppeople_id=people_id).delete()
    if result > 0:
        db.session.commit()
    return jsonify({"message": "Favorite Person deleted"})


# Keep At the Bottom of the File
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
