from sqlalchemy import distinct
from ..persistence.model.BillingAddressModel import BillingAddressModel 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete
from ..persistence.model.PrenotazioniModel import Prenotazioni
from ..persistence.model.PrenotazioneToServiziModel import PrenotazioneToServizi
from ..persistence.model.ServiziModel import Servizi
from ..persistence.model.UserModel import User
from typing import List
from ..persistence.model.DisponibilitaModel import Disponibilita
from datetime import date

def cancella_displibilita_cowork(servizio_id: str, db: Session, dal = None, al = None):

    delete_from = delete(Disponibilita).where(Disponibilita.idServizio == servizio_id)

    if(dal and al):
        # If date range is provided, delete only within that range
        delete_from = delete_from.where(Disponibilita.date >= dal).where(Disponibilita.date <= al)

    elif(dal and not al):
        # If only dal is provided, delete from dal onwards
        delete_from = delete_from.where(Disponibilita.date == dal)


    db.execute(delete_from)
    db.commit()
    return None

def aggiungiDisponibilita(disponibilita: Disponibilita, db: Session):
    db.add(disponibilita)
    db.commit()
    return None

def getDisponibilitaCoWorkService(db: Session, dal: date, al : date , tipologia: str) -> List[tuple[Disponibilita, Servizi]]:
    
    stmt = select(Disponibilita, Servizi)\
            .join(Servizi, Disponibilita.idServizio == Servizi.id)\
            .where(Disponibilita.date >= dal).where(Disponibilita.date <= al)
            
    if(tipologia != 'ALL'):
        stmt = stmt.where(Servizi.id == tipologia)
    
    results = db.execute(stmt).all()
    return results
'''
def getPrenotazioniServiziByDate(db: Session,  dal: date, al : date , idServizi: List[int]) -> List[Prenotazioni]:
    
    stmt = select(Prenotazioni)\
            .join(PrenotazioneToServizi, PrenotazioneToServizi.idPrenotazione == Prenotazioni.id)\
            .where(Prenotazioni.data >= dal).where(Prenotazioni.data <= al)\
            .where(PrenotazioneToServizi.idServizio.in_(idServizi))
    
    results = db.execute(stmt).scalars().all()
    return results
'''