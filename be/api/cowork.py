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
from datetime import date, timedelta, datetime
from ..service.payment_service import aggiungiPagamento
from calendar import monthrange
import random
from ..persistence.model import PaymentModel as payment_models

# Role Based Endpoints
allow_admin_only = auth.RoleChecker(["all"])
allowed_cowork_roles = auth.RoleChecker(["all", "CoWorking"])


router = APIRouter(
    prefix="/cowork",
    tags=["cowork"]
)

@router.get("/servizi", response_model=List[cowork_schema.ServiziCoWorkSchema])
def getServiziCoWork( db: Session = Depends(auth.get_db), user: models.User = Depends(allowed_cowork_roles)):
    stmt = select(Servizi).order_by(Servizi.nome)
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
    user: models.User = Depends(allowed_cowork_roles)
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
    else:
        #periodo è una data
        dal = datetime.strptime(periodo, "%Y-%m-%d").date()
        al = dal


    disponibilita:List[tuple[Disponibilita, Servizi]] = getDisponibilitaCoWorkService(db, dal, al, tipologia)
    
    retcode: List[cowork_schema.DisponibilitaConPrenotazioneSchema] = []
    if len(disponibilita) == 0:
        return []
    
    prenotazioni_giorno = getPrenotazioniServiziByDate(db, dal, al, disponibilita[0][0].idServizio)
    
    for disponibilitaModel, servizioModel in disponibilita:

        numPrenotazioniMattina = sum(1 for p in prenotazioni_giorno if p.flgMattina and p.data == disponibilitaModel.date)
        numPrenotazioniPomeriggio = sum(1 for p in prenotazioni_giorno if p.flgPomeriggio and p.data == disponibilitaModel.date)

        retcode.append( 
            cowork_schema.DisponibilitaConPrenotazioneSchema(
            idServizio=disponibilitaModel.idServizio,
            date=disponibilitaModel.date,
            numMattina=disponibilitaModel.numMattina,
            numPomeriggio=disponibilitaModel.numPomeriggio,
            nomeServizio=servizioModel.nome,
            numPrenotazioniMattina=numPrenotazioniMattina, 
            numPrenotazioniPomeriggio=numPrenotazioniPomeriggio,
        ))

    return retcode      

@router.get("/disponibilita-month", status_code=200, response_model=List[cowork_schema.DisponibilitaConPrenotazioneSchema])
def getDisponibilitaCoWorkPerIlMese(
    data: date,
    tipologia:str,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allowed_cowork_roles)
):
    
    # Primo e ultimo giorno del mese
    first_day = data.replace(day=1)
    last_day = data.replace(day=monthrange(data.year, data.month)[1])
    disponibilita:List[tuple[Disponibilita, Servizi]] = getDisponibilitaCoWorkService(db, first_day, last_day, None, tipologia)
    retcode: List[cowork_schema.DisponibilitaConPrenotazioneSchema] = []
    if len(disponibilita) == 0:
        return []
    
    prenotazioni_giorno = getPrenotazioniServiziByDate(db, first_day, last_day, disponibilita[0][0].idServizio)

    for disponibilitaModel, servizioModel in disponibilita:
       
        numPrenotazioniMattina = sum(1 for p in prenotazioni_giorno if p.flgMattina and p.data == disponibilitaModel.date)
        numPrenotazioniPomeriggio = sum(1 for p in prenotazioni_giorno if p.flgPomeriggio and p.data == disponibilitaModel.date)

        retcode.append( 
            cowork_schema.DisponibilitaConPrenotazioneSchema(
            idServizio=disponibilitaModel.idServizio,
            date=disponibilitaModel.date,
            numMattina=disponibilitaModel.numMattina - numPrenotazioniMattina,
            numPomeriggio=disponibilitaModel.numPomeriggio - numPrenotazioniPomeriggio,
            nomeServizio=servizioModel.nome,
            numPrenotazioniMattina=0, 
            numPrenotazioniPomeriggio=0,
        ))

    return retcode       


@router.delete("/disponibilita/{idServizio}/{data}", status_code=200)
def eliminaDisponibilita(
    idServizio: str,
    data: str,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allow_admin_only)):

    data_date = datetime.strptime(data, "%Y-%m-%d").date()
    cancella_displibilita_cowork(idServizio, db, data_date, None)
    return True


@router.post("/prenotazione", status_code=200)
def salvaPrenotazione(
    prenotazione:cowork_schema.NewPrenotazioneCoWorkSchema,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allowed_cowork_roles)
):
    
    if( creaPrenotazioneCoWorkFromSchema(db, prenotazione)):
        
        aggiungiPagamento(db, 
            payment_models.Payment(
                userId=prenotazione.userId,
                paymentId = f"PAY-{random.randint(100, 99999999)}",
                value=prenotazione.pagamento.value,
                status=prenotazione.pagamento.status.upper(),
                date=prenotazione.pagamento.date,
                tipoPagamento=prenotazione.pagamento.tipoPagamento.upper()
            )
        )
        return True
    else:
        raise HTTPException(status_code=400, detail="Errore durante la creazione della prenotazione")

@router.get("/prenotazioni", status_code=200, response_model=List[cowork_schema.PrenotazioneCoWorkDetailSchema])
def getPrenotazioni(
    data: date,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allowed_cowork_roles)
):
    return getPrenotazioniWithDetailsByDate(db, data)

@router.delete("/prenotazioni/{id}", status_code=204)
def deletePrenotazioneEndpoint(
    id: str,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(allowed_cowork_roles)
):
    deletePrenotazione(db, id)
    return None


@router.get("/next-user-co-workings", status_code=200, response_model=List)
def getNextUserCoWorkings(
    userId: str = None,
    db: Session = Depends(auth.get_db),
    user: models.User = Depends(auth.get_current_user)
):
    
    target_user_id = user.id
    if user.userType == 'admin' and userId:
        target_user_id = userId

    if(target_user_id):
        return getUserCoWorkings(db, target_user_id, date.today(), date.today() + timedelta(days=90))




    