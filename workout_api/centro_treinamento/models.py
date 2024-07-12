from sqlalchemy import Column, Integer, String
from app.database import Base

class CentroTreinamentoModel(Base):
    __tablename__ = "centro_treinamento"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    localizacao = Column(String)
