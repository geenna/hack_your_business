from pydantic import BaseModel
from datetime import date
from typing import Optional
from .PaymentSchema import PaymentCreate
from .UserSchema import UserResponse

class ServiziCoWorkSchema(BaseModel):
    id: str
    nome: str
    key: str
    costoIntero: float
    costoRidotto: float
   
    class Config:
        from_attributes = True

class PrenotazioneCoWorkDetailSchema(BaseModel):
    id: str
    data: date
    flgMattina: bool
    flgPomeriggio: bool
    pin: str
    wifiAccess: str
    user: UserResponse
    servizi: list[ServiziCoWorkSchema]

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

class NewPrenotazioneCoWorkSchema(BaseModel):
    idServizioSelezionato: str
    date: list[str]
    turno: str
    userId: str
    pagamento: PaymentCreate
    tipologia: str

    class Config:
        from_attributes = True


        