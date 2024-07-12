from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from workout_api.database import Base

class AtletaModel(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    centro_treinamento_id = Column(Integer, ForeignKey('centros_treinamento.id'))
    centro_treinamento = relationship("CentroTreinamentoModel", back_populates="atletas")
