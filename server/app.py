import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower

# Set up the base directory and database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Initialize the Flask application
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Optional: Disable JSON compacting for more readable output (useful in development)
app.json.compact = False

# Initialize the database and migration tools
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)

# Root route for testing the API
@app.route('/')
def index():
    """
    A simple route to test if the server is running.
    """
    return '<h1>Code Challenge - API is Running</h1>'

# Error handling route for invalid endpoints
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

# Sample Resource for managing Heroes (you can expand this)
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

# Sample Resource for managing Powers (you can expand this)
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

# Adding routes to Flask-RESTful API
api.add_resource(HeroResource, '/heroes', '/heroes/<int:hero_id>')
api.add_resource(PowerResource, '/powers', '/powers/<int:power_id>')

# Entry point of the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)