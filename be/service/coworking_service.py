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
from fastapi import HTTPException
import random
import string

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
    
    stmt = select(Prenotazioni, PrenotazioneToServizi)\
            .join(PrenotazioneToServizi, PrenotazioneToServizi.idPrenotazione == Prenotazioni.id)\
            .where(Prenotazioni.data.in_(giorni))\
            .where(PrenotazioneToServizi.idServizio == servizioId)

    results = db.execute(stmt).all()
    if(len(results) == 0):
        return []
    
    return results

def setPrenotazione(db: Session, prenotazione: Prenotazioni) -> Prenotazioni:
    
    db.add(prenotazione)
    db.commit()
    db.refresh(prenotazione)
    return prenotazione

def setPrenotazioneToServizi(db: Session, prenotazioneToServizi: PrenotazioneToServizi) -> PrenotazioneToServizi:
    
    db.add(prenotazioneToServizi)
    db.commit()
    db.refresh(prenotazioneToServizi)
    return prenotazioneToServizi    

def getDisponibilitaCompletaByDate(db: Session, date: List[date], servizioId: str) -> Disponibilita:
    
    disponibilitaServizio = getDisponibilitaGiorniServizio(db, date, servizioId)

    if(disponibilitaServizio is None or len(disponibilitaServizio) == 0):
        raise HTTPException(status_code=400, detail="Disponibilità non trovata. Riprovare a fare la prenotazione.")

    disponibilitaByDate:dict[date, Disponibilita] = {d.date: d for (d, s) in disponibilitaServizio}
    
    prenotazioniEsistenti:List[Prenotazioni] = getPrenotazioniGiorniServizio(db, date, servizioId)
    prenotazioniByDate: dict[date, List[Prenotazioni]] = {}
    for (p, s) in prenotazioniEsistenti:
        if p.data not in prenotazioniByDate:
            prenotazioniByDate[p.data] = []
        prenotazioniByDate[p.data].append(p)
        
    mappa_disponibilita = {}
    for d, disp in disponibilitaByDate.items():
        m = disp.numMattina
        p = disp.numPomeriggio
        for pren in prenotazioniByDate.get(d, []):
            if pren.flgMattina:
                m -= 1
            if pren.flgPomeriggio:
                p -= 1
        mappa_disponibilita[d] = {"mattina": m, "pomeriggio": p}
    
    return mappa_disponibilita
    




def creaPrenotazioneCoWorkFromSchema(db: Session, prenotazione: cowork_schema.NewPrenotazioneCoWorkSchema):
    
    mappaDisponibilitaReale = getDisponibilitaCompletaByDate(db, [datetime.strptime(d, "%Y-%m-%d").date() for d in prenotazione.date], prenotazione.idServizioSelezionato)

    pinAccesso = random.randint(100000, 999999)
    wifiAccess = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 12)))

    for item in prenotazione.date:    
        flgMattina = False
        flgPomeriggio = False

        if(prenotazione.turno == "INTERO_GIORNO" or prenotazione.turno == "MATTINA"):
            flgMattina = True
        if(prenotazione.turno == "INTERO_GIORNO" or prenotazione.turno == "POMERIGGIO"):
            flgPomeriggio = True
        
        current_date = datetime.strptime(item, "%Y-%m-%d").date()
        if current_date not in mappaDisponibilitaReale or \
           (flgMattina and mappaDisponibilitaReale[current_date]["mattina"] <= 0) or \
           (flgPomeriggio and mappaDisponibilitaReale[current_date]["pomeriggio"] <= 0):
            raise HTTPException(status_code=400, detail="Disponibilità non disponibile per la data o il turno selezionato.")
        
        
        prenotazioneModel = Prenotazioni(
            userId = prenotazione.userId,
            flgMattina = flgMattina,
            flgPomeriggio = flgPomeriggio,
            data = datetime.strptime(item, "%Y-%m-%d").date(),
            pin = pinAccesso,
            wifiAccess = wifiAccess
        )
        prenotazioneNew = setPrenotazione(db, prenotazioneModel)
        prenotazioneToServizi = PrenotazioneToServizi(
            idPrenotazione = prenotazioneNew.id,
            idServizio = prenotazione.idServizioSelezionato
        )
        prenotazioneToServizi = setPrenotazioneToServizi(db, prenotazioneToServizi) 

    return True
    

def getPrenotazioniServiziByDate(db: Session,  dal: date, al : date , idServizi: int) -> List[Prenotazioni]:
    
    stmt = select(Prenotazioni)\
            .join(PrenotazioneToServizi, PrenotazioneToServizi.idPrenotazione == Prenotazioni.id)\
            .where(Prenotazioni.data >= dal).where(Prenotazioni.data <= al)\
            .where(PrenotazioneToServizi.idServizio == idServizi)
    
    results = db.execute(stmt).scalars().all()
    return results

def getPrenotazioniWithDetailsByDate(db: Session, data: date):
    # Fetch Prenotazioni + User
    stmt = select(Prenotazioni, User).join(User, Prenotazioni.userId == User.id).where(Prenotazioni.data == data)
    results = db.execute(stmt).all()
    
    if not results:
        return []

    prenotazioni_map = {}
    for pren, user in results:
        prenotazioni_map[pren.id] = {
            "id": pren.id,
            "data": pren.data,
            "flgMattina": pren.flgMattina,
            "flgPomeriggio": pren.flgPomeriggio,
            "pin": pren.pin,
            "wifiAccess": pren.wifiAccess,
            "user": user,
            "servizi": []
        }

    pren_ids = list(prenotazioni_map.keys())

    # Fetch services
    stmt_servizi = select(PrenotazioneToServizi.idPrenotazione, Servizi)\
        .join(Servizi, PrenotazioneToServizi.idServizio == Servizi.id)\
        .where(PrenotazioneToServizi.idPrenotazione.in_(pren_ids))
    
    servizi_results = db.execute(stmt_servizi).all()

    for pren_id, servizio in servizi_results:
        if pren_id in prenotazioni_map:
            prenotazioni_map[pren_id]["servizi"].append(servizio)

    return list(prenotazioni_map.values())

def deletePrenotazione(db: Session, id: str):
    # Delete relations
    stmt_rel = delete(PrenotazioneToServizi).where(PrenotazioneToServizi.idPrenotazione == id)
    db.execute(stmt_rel)
    
    # Delete reservation
    stmt_main = delete(Prenotazioni).where(Prenotazioni.id == id)
    db.execute(stmt_main)
    
    db.commit()
    return True
