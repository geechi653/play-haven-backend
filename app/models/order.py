from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(
        "users.id"), nullable=False)
    game_id = mapped_column(Integer, ForeignKey(
        "games.id"), nullable=False)
    order_date = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    total_amount = mapped_column(Numeric(10, 2), nullable=False)
    status = mapped_column(String(255), nullable=True)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "order_date": self.order_date,
            "total_amount": str(self.total_amount),
            "status": self.status
        }
