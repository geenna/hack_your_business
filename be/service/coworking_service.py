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
from datetime import date, datetime
from ..persistence.schemas import CoWorkSchema as cowork_schema

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

def getDisponibilitaCoWorkService(db: Session, dal: date, al : date , tipologia: str = None, serviziokey: str = None) -> List[tuple[Disponibilita, Servizi]]:
    
    stmt = select(Disponibilita, Servizi)\
            .join(Servizi, Disponibilita.idServizio == Servizi.id)\
            .where(Disponibilita.date >= dal).where(Disponibilita.date <= al)

    if( tipologia is not None):     
        if(tipologia != 'ALL'):
            stmt = stmt.where(Servizi.id == tipologia)
    elif (serviziokey is not None):
        stmt = stmt.where(Servizi.key == serviziokey)  
    
    results = db.execute(stmt).all()
    return results

def getDisponibilitaGiorniServizio(db: Session, giorni: List[date] , servizioId: str) -> List[tuple[Disponibilita, Servizi]]:
    
    stmt = select(Disponibilita, Servizi)\
            .join(Servizi, Disponibilita.idServizio == Servizi.id)\
            .where(Disponibilita.date.in_(giorni))\
            .where(Disponibilita.idServizio == servizioId)

    results = db.execute(stmt).all()
    if(len(results) == 0):
        return []
    
    return results

def getPrenotazioniGiorniServizio(db: Session, giorni: List[date] , servizioId: str) -> List[Prenotazioni]:
    
    stmt = select(Prenotazioni)\
            .join(PrenotazioneToServizi, PrenotazioneToServizi.idPrenotazione == Prenotazioni.id)\
            .where(Prenotazioni.data.in_(giorni))\
            .where(PrenotazioneToServizi.idServizio == servizioId)

    results = db.execute(stmt).all()
    if(len(results) == 0):
        return []
    
    return results

def creaPrenotazioneCoWorkFromSchema(db: Session, prenotazione: cowork_schema.NewPrenotazioneCoWorkSchema):
    
    disponibilita = getDisponibilitaGiorniServizio(db, [datetime.strptime(d, "%Y-%m-%d").date() for d in prenotazione.date], prenotazione.idServizioSelezionato)

    if(disponibilita is None or len(disponibilita) == 0):
        return None
    if(len(disponibilita) != len(prenotazione.date)):
        return None

    prenotazioni = getPrenotazioniGiorniServizio(db, [datetime.strptime(d, "%Y-%m-%d").date() for d in prenotazione.date], prenotazione.idServizioSelezionato)
    
    prenotazioniByDate:dict[date, Prenotazioni] = {p.date: p for p in prenotazioni}
    if(len(prenotazioniByDate) > 0):
        print("verificare tutte le disponibilita se ci sono gia prenotazioni")

    

    

def getPrenotazioniServiziByDate(db: Session,  dal: date, al : date , idServizi: List[int]) -> List[Prenotazioni]:
    
    stmt = select(Prenotazioni)\
            .join(PrenotazioneToServizi, PrenotazioneToServizi.idPrenotazione == Prenotazioni.id)\
            .where(Prenotazioni.data >= dal).where(Prenotazioni.data <= al)\
            .where(PrenotazioneToServizi.idServizio.in_(idServizi))
    
    results = db.execute(stmt).scalars().all()
    return results
