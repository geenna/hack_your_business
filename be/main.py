from fastapi import FastAPI, APIRouter
from .persistence.model import UserModel as user_models
from .persistence.model import PaymentModel as payment_models
from .persistence.model import ProjectModel as project_models
from .persistence.model import BillingAddressModel as billing_models
from .persistence.model import UserToProjectModel as user_project_models
from .persistence.database import engine
from .api import auth, users, payments, test_service, projects

from fastapi.middleware.cors import CORSMiddleware

user_models.Base.metadata.create_all(bind=engine)
billing_models.Base.metadata.create_all(bind=engine)
user_project_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(payments.router)
api_router.include_router(projects.router)
api_router.include_router(test_service.router)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
