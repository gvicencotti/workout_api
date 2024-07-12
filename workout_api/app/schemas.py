from pydantic import BaseModel

class AtletaBase(BaseModel):
    nome: str
    cpf: str

class AtletaCreate(AtletaBase):
    pass

class AtletaSchema(AtletaBase):
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True
