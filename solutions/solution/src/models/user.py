import uuid
from datetime import datetime
from flask import current_app
from solutions.solution.src.persistence.dbinit import db
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    """User class that links to the SQLite table users"""
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    reviews = relationship("Review", back_populates="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email} {self.first_name} {self.last_name} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def set_password(self, password):
        """Hash and set the password"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check hashed password"""
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""
        repo = current_app.repository
        users = repo.get_all(User)
        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")
        new_user = User(
            id=str(uuid.uuid4()),
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            is_admin=user.get("is_admin", False),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        new_user.set_password(user["password"])  # Set the hashed password
        repo.save(new_user)
        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        repo = current_app.repository
        user = repo.get(User, user_id)
        if not user:
            return None
        if "email" in data:
            existing_users = repo.get_all(User)
            for existing_user in existing_users:
                if existing_user.email == data["email"] and existing_user.id != user_id:
                    raise ValueError("Email already exists")
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "password" in data:
            user.set_password(data["password"])  # Set the hashed password
        user.updated_at = datetime.utcnow() 
        repo.update(user)
        return user

    @staticmethod
    def delete(user_id: str) -> bool:
        """Delete a user"""
        repo = current_app.repository
        user = repo.get(User, user_id)
        if not user:
            return False
        repo.delete(user)
        return True

    @staticmethod
    def get_all() -> list:
        """Get all users"""
        repo = current_app.repository
        return repo.get_all(User)

    @staticmethod
    def get(user_id: str) -> "User | None":
        """Get a user by ID"""
        repo = current_app.repository
        return repo.get(User, user_id)
