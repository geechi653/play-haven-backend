from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, Boolean
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(255), unique=True,
                             nullable=False, index=True)
    email = mapped_column(String(255), unique=True, nullable=False, index=True)
    password = mapped_column(String(255), nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)
    is_admin = mapped_column(Boolean, default=False, nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(DateTime, default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")
    user_library_entries = relationship("UserLibrary", back_populates="user")
    wishlist_items = relationship("WishlistItem", back_populates="user")



    def set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
