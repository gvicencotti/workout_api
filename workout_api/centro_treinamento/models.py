# workout_api/centro_treinamento/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from workout_api.database import Base

class CentroTreinamentoModel(Base):
    __tablename__ = "centros_treinamento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    atletas = relationship("AtletaModel", back_populates="centro_treinamento")
