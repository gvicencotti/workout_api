# app/main.py

from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi_pagination import Page, paginate, add_pagination
from fastapi_pagination.limit_offset import LimitOffsetPage, Params
from typing import Optional
from .database import SessionLocal, engine
from .models import Base, Atleta
from .schemas import AtletaSchema, AtletaCreate
from .crud import get_atleta_by_cpf, create_atleta, get_atletas

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/atletas", response_model=LimitOffsetPage[AtletaSchema])
def read_atletas(
    nome: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
    params: Params = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(Atleta)
    if nome:
        query = query.filter(Atleta.nome == nome)
    if cpf:
        query = query.filter(Atleta.cpf == cpf)
    
    atletas = query.all()
    return paginate(atletas, params)

@app.post("/atletas", response_model=AtletaSchema)
def create_new_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    db_atleta = get_atleta_by_cpf(db, cpf=atleta.cpf)
    if db_atleta:
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    try:
        return create_atleta(db=db, atleta=atleta)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

add_pagination(app)
