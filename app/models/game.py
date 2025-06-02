from sqlalchemy import String, DateTime, Integer, Numeric, Float, Text
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class Game(db.Model):
    __tablename__ = "games"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255), nullable=False)
    price = mapped_column(Numeric(10, 2), nullable=False)
    release_year = mapped_column(Integer, nullable=False)
    status = mapped_column(String(255), nullable=True)
    category = mapped_column(String(255), nullable=False)
    description = mapped_column(Text, nullable=True)
    platform = mapped_column(String(255), nullable=False)
    rating = mapped_column(Float, nullable=True)
    image_url = mapped_column(String(255), nullable=True)

    user_library = relationship("UserLibrary", back_populates="user_games")
    wishlist_item = relationship("WishlistItem", back_populates="game")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": str(self.price),
            "release_year": self.release_year,
            "status": self.status,
            "category": self.category,
            "description": self.description,
            "platform": self.platform,
            "rating": self.rating,
            "image_url": self.image_url
        }
