from ..db import BaseDb
from sqlalchemy import Boolean, DateTime, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

class Items(BaseDb):
    __tablename__ = "Items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    price: Mapped[float] = mapped_column(Float, nullable= False)

    color: Mapped[str | None] = mapped_column(String(500), nullable=True)