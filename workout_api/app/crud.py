from sqlalchemy.orm import Session
from .models import Atleta
from .schemas import AtletaCreate

def get_atleta_by_cpf(db: Session, cpf: str):
    return db.query(Atleta).filter(Atleta.cpf == cpf).first()

def create_atleta(db: Session, atleta: AtletaCreate):
    db_atleta = Atleta(**atleta.dict())
    db.add(db_atleta)
    db.commit()
    db.refresh(db_atleta)
    return db_atleta

def get_atletas(db: Session):
    return db.query(Atleta).all()
