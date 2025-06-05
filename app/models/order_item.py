from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    game_id = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    quantity = mapped_column(Integer, nullable=False, default=1)
    price = mapped_column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    game = relationship("Game", back_populates="order_items")

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "game_id": self.game_id,
            "quantity": self.quantity,
            "price": str(self.price)
        }
