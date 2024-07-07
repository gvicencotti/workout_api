from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List, Optional
from fastapi_pagination import Page, add_pagination, paginate
from .models import AtletaModel, CategoriaModel, CentroTreinamentoModel
from .database import get_db

app = FastAPI()

class AtletaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

@app.get("/atletas", response_model=Page[AtletaResponse])
def get_atletas(nome: Optional[str] = Query(None), cpf: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(AtletaModel).join(CentroTreinamentoModel).join(CategoriaModel)
    
    if nome:
        query = query.filter(AtletaModel.nome == nome)
    
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    atletas = query.all()
    response = [
        AtletaResponse(
            nome=atleta.nome,
            centro_treinamento=atleta.centro_treinamento.nome,
            categoria=atleta.categoria.nome
        )
        for atleta in atletas
    ]
    return paginate(response)

class AtletaCreate(BaseModel):
    nome: str
    cpf: str
    idade: int
    peso: float
    altura: float
    sexo: str
    categoria_id: int
    centro_treinamento_id: int

@app.post("/atletas")
def create_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    db_atleta = AtletaModel(**atleta.dict())
    
    try:
        db.add(db_atleta)
        db.commit()
        db.refresh(db_atleta)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    
    return db_atleta

add_pagination(app)
