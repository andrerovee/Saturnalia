from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from ..db import BaseDb

class Terreni(BaseDb):
    __tablename__ = "terreni"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codice_nome: Mapped[str] = mapped_column(String(100), nullable=False)
    comune: Mapped[str] = mapped_column(String(100), nullable=False)
    area_coltivata_m2: Mapped[float] = mapped_column(Float, nullable=False)
    
    particelle = relationship("Particelle", back_populates="terreno")

class Particelle(BaseDb):
    __tablename__ = "particelle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    terreno_id: Mapped[int] = mapped_column(Integer, ForeignKey("terreni.id"))
    comune: Mapped[str] = mapped_column(String(100), nullable=False)
    sezione: Mapped[str | None] = mapped_column(String(10), nullable=True)
    foglio: Mapped[int] = mapped_column(Integer, nullable=False)
    particella: Mapped[int] = mapped_column(Integer, nullable=False)
    superficie_m2: Mapped[float] = mapped_column(Float, nullable=False)

    terreno = relationship("Terreni", back_populates="particelle")
