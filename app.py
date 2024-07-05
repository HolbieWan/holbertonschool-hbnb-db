import os
from flask import Flask
from config import config
#from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from solutions.solution.src.persistence import get_repository
from solutions.solution.src.persistence.db import DBRepository
from solutions.solution.src.persistence.dbinit import db

def create_app():
    #load_dotenv()

    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    app.config['JWT_SECRET_KEY'] = 'My_secret_key'
    jwt = JWTManager(app)
    env = os.getenv('FLASK_ENV', 'development')
    repo_env = os.getenv('REPOSITORY_ENV_VAR', 'memory')
    print(f"FLASK_ENV is set to: {env}")
    print(f"REPOSITORY_ENV_VAR is set to: {repo_env}")
    app.config.from_object(config[env])
    print(f"App config: {app.config['SQLALCHEMY_DATABASE_URI']}")

    repo = get_repository()
    app.repository = repo
    print(f"Using {repo.__class__.__name__} as repository")

    if isinstance(repo, DBRepository):
        print("Initializing DBRepository")
        db.init_app(app)
        print("DB initialized")
        Migrate(app, db)
        print("Migrate initialized")

        with app.app_context():
            from solutions.solution.src.models.user import User
            from solutions.solution.src.models.country import Country
            from solutions.solution.src.models.city import City
            from solutions.solution.src.models.place import Place
            from solutions.solution.src.models.amenity import Amenity, PlaceAmenity
            from solutions.solution.src.models.review import Review

            db.create_all()
            print("DB tables created")

    from solutions.solution.src.controllers.users import users_bp
    from solutions.solution.src.controllers.countries import country_bp
    from solutions.solution.src.controllers.cities import cities_bp
    from solutions.solution.src.controllers.places import places_bp
    from solutions.solution.src.controllers.amenities import amenities_bp
    from solutions.solution.src.controllers.reviews import reviews_bp
    from solutions.solution.src.controllers.authentication import auth_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(country_bp, url_prefix='/countries')
    app.register_blueprint(cities_bp, url_prefix='/cities')
    app.register_blueprint(places_bp, url_prefix='/places')
    app.register_blueprint(amenities_bp, url_prefix='/amenities')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
