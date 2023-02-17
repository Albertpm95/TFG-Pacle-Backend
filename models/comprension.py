from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Comprension(Base):
    __tablename__ = "comprension"

    id_comprension = Column(String, nullable=False, primary_key=True)
    observaciones = Column(String)
    porcentaje = Column(Integer, nullable=False, default=0)
    puntos_conseguidos = Column(Integer, nullable=False, default=0)
    puntuacion_maxima_parte = Column(Integer, nullable=False, default=0)
    puntuacion_tarea_1 = Column(Integer, nullable=False, default=0)
    puntuacion_tarea_2 = Column(Integer, nullable=False, default=0)
    puntuacion_tarea_3 = Column(Integer, nullable=False, default=0)
    id_acta = Column(String, ForeignKey("Pacle_db.actas.id_acta"), nullable=False)