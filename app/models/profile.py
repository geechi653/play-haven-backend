from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(
        "users.id"), unique=True, nullable=False)
    first_name = mapped_column(String(255), nullable=True)
    last_name = mapped_column(String(255), nullable=True)
    avatar_url = mapped_column(String(255), nullable=True)
    address = mapped_column(String(255), nullable=True)
    city = mapped_column(String(255), nullable=True)
    state = mapped_column(String(100), nullable=True)
    zip_code = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="profile")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar_url": self.avatar_url,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code
        }
