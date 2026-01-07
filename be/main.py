from fastapi import FastAPI
from .persistence.model import UserModel as user_models
from .persistence.model import PaymentModel as payment_models
from .persistence.model import ProjectModel as project_models
from .persistence.database import engine
from .api import auth, users, payments, test_service

from fastapi.middleware.cors import CORSMiddleware

user_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(payments.router)
app.include_router(test_service.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
