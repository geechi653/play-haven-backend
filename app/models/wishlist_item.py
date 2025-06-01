from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(
        "users.id"), unique=True, nullable=False)
    game_id = mapped_column(Integer, ForeignKey(
        "games.id"), unique=True, nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    game = relationship("Game", back_populates="wishlist_item")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "created_at": self.order_date,
        }
