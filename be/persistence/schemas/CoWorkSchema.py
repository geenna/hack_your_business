from pydantic import BaseModel
from datetime import date
from typing import Optional

class ServiziCoWorkSchema(BaseModel):
    id: str
    nome: str
    key: str
    costoIntero: float
    costoRidotto: float
   
    class Config:
        from_attributes = True

class DisponibilitaCoWorkSchema(BaseModel):
    idServizio: str
    date: date
    numMattina: int
    numPomeriggio: int
    servizio: Optional[ServiziCoWorkSchema] = None

    class Config:
        from_attributes = True

   
