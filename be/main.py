from fastapi import FastAPI, APIRouter
from .persistence.model import UserModel as user_models
from .persistence.model import PaymentModel as payment_models
from .persistence.model import ProjectModel as project_models
from .persistence.model import BillingAddressModel as billing_models
from .persistence.model import UserToProjectModel as user_project_models
from .persistence.model import UserDocumentModel as user_document_models
from .persistence.model import ProjectDocumentModel as project_document_models
from .persistence.model import PrenotazioniModel as prenotazioni_models
from .persistence.model import PrenotazioneToServiziModel as prenotazione_to_servizi_models
from .persistence.model import ServiziModel as servizi_models
from .persistence.model import DisponibilitaModel as disponibilita_models
from .persistence.database import engine
from .api import auth, cowork, users, payments, test_service, projects, repository

from fastapi.middleware.cors import CORSMiddleware

user_models.Base.metadata.create_all(bind=engine)
billing_models.Base.metadata.create_all(bind=engine)
user_project_models.Base.metadata.create_all(bind=engine)
user_document_models.Base.metadata.create_all(bind=engine)
project_document_models.Base.metadata.create_all(bind=engine)
prenotazioni_models.Base.metadata.create_all(bind=engine)
prenotazione_to_servizi_models.Base.metadata.create_all(bind=engine)
servizi_models.Base.metadata.create_all(bind=engine)
disponibilita_models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Hack Your Business API",
    description="API for Hack Your Business application",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(payments.router)
api_router.include_router(projects.router)
api_router.include_router(test_service.router)
api_router.include_router(repository.router)
api_router.include_router(cowork.router)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
