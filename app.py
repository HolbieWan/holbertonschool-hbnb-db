"""Main application file """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///hbnb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['USE_DATABASE'] = os.getenv('USE_DATABASE', 'True').lower() in ['true', '1', 'yes']

# Initialize the database
db = SQLAlchemy(app)

# Register routes



if __name__ == '__main__':
    app.run(debug=True)
