from fastapi import FastAPI, Depends
from app.api import (
    agenda_routes,
    reserva_routes
)

app = FastAPI()
app.title = "API agendamentos"

app.include_router(agenda_routes.router, prefix="/agendar", tags=["agendar"])
app.include_router(reserva_routes.router, prefix="/reserva", tags=["reserva"])

@app.get("/")
def index():
    return {"message": "Bem vindo a API de agendamentos"}