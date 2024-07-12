from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Atleta
from .schemas import AtletaCreate

def get_atleta_by_cpf(db: Session, cpf: str):
    return db.query(Atleta).filter(Atleta.cpf == cpf).first()

def create_atleta(db: Session, atleta: AtletaCreate):
    try:
        db_atleta = Atleta(**atleta.dict())
        db.add(db_atleta)
        db.commit()
        db.refresh(db_atleta)
        return db_atleta
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

def get_atletas(db: Session, nome: str = None, cpf: str = None):
    query = db.query(Atleta)
    if nome:
        query = query.filter(Atleta.nome == nome)
    if cpf:
        query = query.filter(Atleta.cpf == cpf)
    return query.all()
