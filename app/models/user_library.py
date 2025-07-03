from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class UserLibrary(db.Model):
    __tablename__ = "user_library"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    steam_game_id = mapped_column(Integer, nullable=False)  # Store Steam game ID directly
    added_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_library_entries")

    __table_args__ = (
        db.UniqueConstraint('user_id', 'steam_game_id', name='unique_user_steam_game_library'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "steam_game_id": self.steam_game_id,
            "added_at": self.added_at,
        }