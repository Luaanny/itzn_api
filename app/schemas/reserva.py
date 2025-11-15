from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from datetime import date
from app.core.security import VALID_START_HOUR

class CriarReserva(BaseModel):
    data_reserva: date
    hora_inicio: VALID_START_HOUR
    justificativa: str
    email_usuario: EmailStr
    model_config = ConfigDict(from_attributes=True)

class RespostaReserva(BaseModel):
    id: int
    data_reserva: date
    hora_inicio: VALID_START_HOUR
    justificativa: str
    email_usuario: EmailStr

class ListaReserva(BaseModel):
    reservas: List[RespostaReserva]