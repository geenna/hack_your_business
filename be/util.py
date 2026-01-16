from typing import List
from .persistence.model.ProjectModel import Projects
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

def statistiche_progetti(progetti:List[Projects]):
    numScaduti = 0
    numInCorso = 0
    numCompletati = 0
    numInScadenza = 0
    for progetto in progetti:

        if progetto.avanzamento == 100:
            numCompletati += 1
        elif progetto.datFine and progetto.datFine < datetime.now():
            numScaduti += 1
        elif progetto.datFine and progetto.datFine < datetime.now() + timedelta(days=30):
            numInScadenza += 1
        else:
            numInCorso += 1

    return {"numScaduti": numScaduti, "numInScadenza": numInScadenza, "numInCorso": numInCorso, "numCompletati": numCompletati}
    