from flask import Flask
from config import config
from flask_migrate import Migrate
import os
from solutions.solution.src.persistence import get_repository
from solutions.solution.src.persistence.db import DBRepository  # Import DBRepository for isinstance check

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    repo_env = os.getenv('REPOSITORY_ENV_VAR', 'memory')
    print(f"FLASK_ENV is set to: {env}")
    print(f"REPOSITORY_ENV_VAR is set to: {repo_env}")
    app.config.from_object(config[env])
    print(f"App config: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize the appropriate repository
    repo = get_repository()
    app.repository = repo
    print(f"Using {repo.__class__.__name__} as repository")

    if isinstance(repo, DBRepository):
        print("Initializing DBRepository")
        from solutions.solution.src.persistence.dbinit import db  # Import db from db_init
        db.init_app(app)
        Migrate(app, db)  # Initialize Flask-Migrate

        with app.app_context():
            # Import models here to ensure they are detected by Alembic
            from solutions.solution.src.models.user import User
            from solutions.solution.src.models.country import Country
            from solutions.solution.src.models.city import City
            from solutions.solution.src.models.place import Place
            from solutions.solution.src.models.amenity import Amenity, PlaceAmenity
            from solutions.solution.src.models.review import Review

            db.create_all()  # Create tables for our models

    # Import and register blueprints here
    from solutions.solution.src.controllers.users import users_bp
    from solutions.solution.src.controllers.countries import country_bp
    from solutions.solution.src.controllers.cities import cities_bp
    from solutions.solution.src.controllers.places import places_bp
    from solutions.solution.src.controllers.amenities import amenities_bp
    from solutions.solution.src.controllers.reviews import reviews_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(country_bp, url_prefix='/countries')
    app.register_blueprint(cities_bp, url_prefix='/cities')
    app.register_blueprint(places_bp, url_prefix='/places')
    app.register_blueprint(amenities_bp, url_prefix='/amenities')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
