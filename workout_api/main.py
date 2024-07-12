# workout_api/main.py
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import add_pagination, paginate
from fastapi_pagination.limit_offset import LimitOffsetPage, LimitOffsetParams
from pydantic import BaseModel
from sqlalchemy.orm import Session
from workout_api.database import SessionLocal, engine, Base
import workout_api.models as models

app = FastAPI()

class AtletaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True

def buscar_atletas(nome: str, cpf: str, params: LimitOffsetParams, db: Session):
    query = db.query(models.AtletaModel)
    if nome:
        query = query.filter(models.AtletaModel.nome == nome)
    if cpf:
        query = query.filter(models.AtletaModel.cpf == cpf)
    return paginate(query.all(), params)

@app.get("/atletas/", response_model=LimitOffsetPage[AtletaResponse])
async def get_atletas(nome: str = Query(None), cpf: str = Query(None), params: LimitOffsetParams = Depends()):
    db = SessionLocal()
    try:
        atletas = buscar_atletas(nome, cpf, params, db)
    finally:
        db.close()
    return atletas

def criar_novo_atleta(atleta_data: dict, db: Session):
    novo_atleta = models.AtletaModel(**atleta_data)
    db.add(novo_atleta)
    db.commit()
    db.refresh(novo_atleta)
    return novo_atleta

class AtletaCreate(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

@app.post("/atletas/")
async def criar_atleta(atleta: AtletaCreate):
    db = SessionLocal()
    try:
        novo_atleta = criar_novo_atleta(atleta.dict(), db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    finally:
        db.close()
    return novo_atleta

add_pagination(app)
