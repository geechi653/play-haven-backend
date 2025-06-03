from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class UserLibrary(db.Model):
    __tablename__ = "user_library"

    id = mapped_column(Integer, primary_key=True)
    added_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    user_id = mapped_column(Integer, ForeignKey(
        "users.id"), unique=True, nullable=False)
    game_id = mapped_column(Integer, ForeignKey(
        "games.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="user_library_entries")
    user_library_entries = relationship("UserLibrary", back_populates="user")
    orders = relationship("Order", back_populates="user_library")

    def serialize(self):
        return {
            "id": self.id,
            "added_at": self.added_at,
            "user_id": self.user_id,
            "game_id": self.game_id,
        }
