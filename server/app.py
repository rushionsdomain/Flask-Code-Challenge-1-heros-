import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower

#database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Initialize Flask 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

@app.route('/')
def index():
    """
    A simple route to test if the server is running.
    """
    return '<h1>Code Challenge - API is Running</h1>'

@app.errorhandler(404)
def not_found(error):
    """
    Custom error handler for 404 - Not Found.
    """
    return jsonify({"error": "Resource not found"}), 404

# Error handling for internal server errors
@app.errorhandler(500)
def internal_error(error):
    """
    Custom error handler for 500 - Internal Server Error.
    """
    return jsonify({"error": "An unexpected error occurred"}), 500

class HeroResource(Resource):
    def get(self, hero_id=None):
        """
        GET request to retrieve hero information.
        If `hero_id` is provided, return that specific hero; otherwise, return all heroes.
        """
        if hero_id:
            hero = Hero.query.get(hero_id)
            if hero:
                return jsonify(hero.to_dict())
            return jsonify({"error": "Hero not found"}), 404
        
        # Get all heroes
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

    def post(self):
        """
        POST request to create a new hero.
        """
        data = request.get_json()
        try:
            hero = Hero(name=data['name'], super_name=data['super_name'])
            db.session.add(hero)
            db.session.commit()
            return jsonify(hero.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class PowerResource(Resource):
    def get(self, power_id=None):
        """
        GET request to retrieve power information.
        If `power_id` is provided, return that specific power; otherwise, return all powers.
        """
        if power_id:
            power = Power.query.get(power_id)
            if power:
                return jsonify(power.to_dict())
            return jsonify({"error": "Power not found"}), 404
        
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

    def post(self):
        """
        POST request to create a new power.
        """
        data = request.get_json()
        try:
            power = Power(name=data['name'], description=data['description'])
            db.session.add(power)
            db.session.commit()
            return jsonify(power.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

api.add_resource(HeroResource, '/heroes', '/heroes/<int:hero_id>')
api.add_resource(PowerResource, '/powers', '/powers/<int:power_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)