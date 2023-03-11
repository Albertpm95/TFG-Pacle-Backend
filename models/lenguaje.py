from sqlalchemy import Column, String, Integer
from db.database import Base


class Lenguaje(Base):
    __tablename__ = "lenguajes"

    id_lenguaje = Column(Integer, primary_key=True)
    lenguaje = Column(String, nullable=False)