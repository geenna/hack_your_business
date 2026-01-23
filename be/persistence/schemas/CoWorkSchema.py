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

   
class NewDisponibilitaCoWorkSchema(BaseModel):
    idServizio: str
    date: list[date]
    numMattina: int
    numPomeriggio: int
    giorniSettimana: list[int]

    class Config:
        from_attributes = True

class DisponibilitaConPrenotazioneSchema(DisponibilitaCoWorkSchema):
    numPrenotazioniMattina: int = 0
    numPrenotazioniPomeriggio: int = 0
    nomeServizio: str

    class Config:
        from_attributes = True