"""
User related functionality
"""

from solutions.solution.src import db

class User(db.Model):
    """State class that links to the SQLite table User"""
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Ensure secure storage
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email} {self.created_at} {self.updated_at})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""
        from src.persistence import repo

        if User.query.filter_by(email=user["email"]).first():
            raise ValueError("User already exists")

        new_user = User(**user)
        repo.save(new_user)
        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        from src.persistence import repo

        user = User.query.get(user_id)
        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = data["password"]  # Consider hashing the password
        if "is_admin" in data:
            user.is_admin = data["is_admin"]

        repo.update(user)
        return user

    @staticmethod
    def get(user_id: str) -> "User | None":
        """Get a user by ID"""
        return User.query.get(user_id)

    @staticmethod
    def get_all() -> list["User"]:
        """Get all users"""
        return User.query.all()

    @staticmethod
    def delete(user_id: str) -> bool:
        """Delete a user by ID"""
        from src.persistence import repo

        user = User.query.get(user_id)
        if not user:
            return False

        repo.delete(user)
        return True
