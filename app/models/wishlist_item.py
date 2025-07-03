from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    steam_game_id = mapped_column(Integer, nullable=False)  # Store Steam game ID directly
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="wishlist_items")

    __table_args__ = (
        db.UniqueConstraint('user_id', 'steam_game_id', name='unique_user_steam_game_wishlist'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "steam_game_id": self.steam_game_id,
            "created_at": self.created_at,
        }