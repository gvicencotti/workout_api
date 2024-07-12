from fastapi import FastAPI, Query, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi_pagination import add_pagination, Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from workout_api.database import get_db
from workout_api.models import Atleta, AtletaCreate
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

app = FastAPI()
add_pagination(app)

class AtletaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

@app.get("/atletas", response_model=Page[AtletaResponse])
async def get_atletas(nome: str = Query(None), cpf: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(Atleta)
    if nome:
        query = query.filter(Atleta.nome == nome)
    if cpf:
        query = query.filter(Atleta.cpf == cpf)
    return sqlalchemy_paginate(query)

@app.post("/atletas")
async def create_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    try:
        db_atleta = Atleta(nome=atleta.nome, centro_treinamento=atleta.centro_treinamento, categoria=atleta.categoria)
        db.add(db_atleta)
        db.commit()
        return {"message": "Atleta criado com sucesso"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=303,
        content={"message": f"Já existe um atleta cadastrado com o cpf: {exc.orig.diag.message_detail}"}
    )
