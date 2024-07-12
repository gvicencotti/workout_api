from fastapi import FastAPI, Query, Request, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from models import Atleta, AtletaCreate
from database import get_db

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
        db.add(atleta)
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
