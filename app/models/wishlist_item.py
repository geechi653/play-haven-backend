from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="wishlist_items")
    game = relationship("Game", back_populates="wishlist_items")

    __table_args__ = (
        db.UniqueConstraint('user_id', 'game_id', name='unique_user_game_wishlist'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "created_at": self.created_at,
        }