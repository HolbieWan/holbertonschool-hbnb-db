# HBnB Evolution: Part 2 (Database Persistence)

## Description of the project
Enhance our application by integrating a relational database using SQLAlchemy, an Object-Relational Mapper (ORM), and by implementing security measures through JWT authentication.

## Evironment
- Operating system : Ubuntu 20.04 LTS
- Virtual Environment : hbtn2
- Flask : flask_sqlalchemy, flask_migrate, flask_bcrypt, flask_jwt_extended

## Project specifitacation

### Integrating SQLAlchemy:
Modify the application to include SQLAlchemy, setting up models to interact with a database while keeping the option for file-based persistence.
Ensure that all models are correctly transformed into SQLAlchemy ORM-compatible classes.
Configure SQLAlchemy to connect to a SQLite database for development purposes.

### Configurable Database Selection:
Implement a configuration system that allows the application to toggle between using SQLite for development and a more robust database like PostgreSQL for production.
Ensure the application can dynamically choose the database type based on environment settings or configuration files.

### Implementing Authentication with JWT:
Integrate Flask-JWT-Extended to add secure authentication mechanisms to the API.
Create endpoints for user authentication that issue JWTs and use these tokens to control access to various API endpoints.

### Database Schema Design and Migration:
Design a database schema that accurately represents the data relationships and business rules.
Create the SQL scripts for your database structure. Optionally, use tools like Alembic to manage database migrations.

### Role-Based Access Control:
Modify existing API endpoints to incorporate checks for user roles and permissions, restricting certain actions to authenticated users or administrators.

### Docker Integration:
Update the Docker configuration to support the new database and authentication functionalities.
Ensure that the Docker environment is configured to handle different database types and authentication services.

## Exemples :
```
$ python3 -m tests.run_all
# ------------------------- #
Results (Passed/Total):
Implement the User Management Endpoints (5/5):
Score: 100.0%
Implement the Country and City Management Endpoints (8/8):
Score: 100.0%
Implement the Amenity Management Endpoints (5/5):
Score: 100.0%
Implement the Places Management Endpoints (5/5):
Score: 100.0%
Implement the Review Management Endpoints (6/6):
Score: 100.0%
```

Created by : 
- [Anthony Cointre](https://github.com/AnthonyCointre/)
- [Cédric Tobie](https://github.com/HolbieWan/)
- [Enzo De Freitas](https://github.com/psychohight/)