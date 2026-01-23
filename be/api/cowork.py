from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from .. import auth
from ..persistence.model import UserModel as models
from ..persistence.model.ServiziModel import Servizi
from ..persistence.model.DisponibilitaModel import Disponibilita
from ..persistence.schemas import UserSchema as user_schema
from ..persistence.schemas import CoWorkSchema as cowork_schema
from ..service.coworking_service import *
from datetime import date, timedelta
# Role Based Endpoints
allow_admin_only = auth.RoleChecker(["all"])
allow_user_only = auth.RoleChecker(["user"])


router = APIRouter(
    prefix="/cowork",
    tags=["cowork"]
)

@router.get("/servizi", response_model=List[cowork_schema.ServiziCoWorkSchema])
def getServiziCoWork( db: Session = Depends(auth.get_db), user: models.User = Depends(auth.get_current_user)):
    stmt = select(Servizi)
    results = db.execute(stmt).scalars().all()
    return results

@router.post("/servizi", response_model=cowork_schema.ServiziCoWorkSchema)
def upsertServizioCoWork(
    servizio: cowork_schema.ServiziCoWorkSchema,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_admin_only)
):
    db_servizio = None
    if servizio.id and servizio.id.strip():
        stmt = select(Servizi).where(Servizi.id == servizio.id)
        db_servizio = db.execute(stmt).scalars().first()

    if db_servizio:
        db_servizio.nome = servizio.nome
        db_servizio.key = servizio.key
        db_servizio.costoIntero = servizio.costoIntero
        db_servizio.costoRidotto = servizio.costoRidotto
    else:
        create_kwargs = {
            "nome": servizio.nome,
            "key": servizio.key,
            "costoIntero": servizio.costoIntero,
            "costoRidotto": servizio.costoRidotto,
        }
        if servizio.id and servizio.id.strip():
            create_kwargs["id"] = servizio.id
        db_servizio = Servizi(**create_kwargs)
        db.add(db_servizio)

    db.commit()
    db.refresh(db_servizio)
    return db_servizio

@router.delete("/servizi/{servizio_id}", status_code=204)
def deleteServizioCoWork(
    servizio_id: str,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_admin_only)
):
    servizio = db.query(Servizi).filter(Servizi.id == servizio_id).first()
    if not servizio:
        raise HTTPException(status_code=404, detail="Servizio not found")
    db.delete(servizio)
    db.commit()
    return None


@router.post("/disponibilita", status_code=200)
def salvaDisponibilita(
    disponibilita: cowork_schema.NewDisponibilitaCoWorkSchema,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_admin_only)
):
    

    servizio = db.query(Servizi).filter(Servizi.id == disponibilita.idServizio).first()
    if(servizio is None):
        raise HTTPException(status_code=404, detail="Servizio non trovato")

    if disponibilita.date and len(disponibilita.date) == 2:
        cancella_displibilita_cowork(disponibilita.idServizio, db, disponibilita.date[0], disponibilita.date[1])
    elif disponibilita.date and len(disponibilita.date) == 1:
        cancella_displibilita_cowork(disponibilita.idServizio, db, disponibilita.date[0], None)

    
    listaServizi = []
    
    if disponibilita.date and len(disponibilita.date) >= 1:
        from datetime import timedelta
        data_inizio = disponibilita.date[0]
        data_fine = disponibilita.date[1] if len(disponibilita.date) == 2 else disponibilita.date[0]
        
        data_corrente = data_inizio
        while data_corrente <= data_fine:
            if data_corrente.weekday() in disponibilita.giorniSettimana:
                
                disponibilitaModel : Disponibilita = Disponibilita(
                    idServizio=disponibilita.idServizio,
                    date=data_corrente,
                    numMattina=disponibilita.numMattina,
                    numPomeriggio=disponibilita.numPomeriggio
                )   
                aggiungiDisponibilita(disponibilitaModel, db)
            data_corrente += timedelta(days=1)

        print(listaServizi)

    return None


@router.get("/disponibilita", status_code=200, response_model=List[cowork_schema.DisponibilitaConPrenotazioneSchema])
def getDisponibilitaCoWork(
    periodo:str,
    tipologia:str,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(auth.get_current_user)
):
    
    dal = date.today()
    al = date.today()

    if(periodo == '30_DAYS'):
        al = dal + timedelta(days=30)
    elif(periodo == '60_DAYS'):
        al = dal + timedelta(days=60)
    elif(periodo == '90_DAYS'):
        al = dal + timedelta(days=90)
    elif(periodo == '6_MONTHS'):
        al = dal + timedelta(days=180)
    elif(periodo == '12_MONTHS'):
        al = dal + timedelta(days=365)


    disponibilita:List[tuple[Disponibilita, Servizi]] = getDisponibilitaCoWorkService(db, dal, al, tipologia)
    retcode: List[cowork_schema.DisponibilitaConPrenotazioneSchema] = []
    if len(disponibilita) == 0:
        return []
    
    #prenotazioni:List[Prenotazioni] = getPrenotazioniServiziByDate(db,  dal, al , [d.idServizio for d in disponibilita[0]])

    for disponibilitaModel, servizioModel in disponibilita:
       
        retcode.append( 
            cowork_schema.DisponibilitaConPrenotazioneSchema(
            idServizio=disponibilitaModel.idServizio,
            date=disponibilitaModel.date,
            numMattina=disponibilitaModel.numMattina,
            numPomeriggio=disponibilitaModel.numPomeriggio,
            nomeServizio=servizioModel.nome,
            numPrenotazioniMattina=0, 
            numPrenotazioniPomeriggio=0 
        ))

    
    return retcode      