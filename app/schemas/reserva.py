from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from datetime import date


class CriarReserva(BaseModel):
    data_reserva: date
    justificativa: str
    email_usuario: EmailStr
    model_config = ConfigDict(from_attributes=True)

class RespostaReserva(BaseModel):
    id: int
    data_reserva: date
    justificativa: str
    email_usuario: EmailStr

class ListaReserva(BaseModel):
    reservas: List[RespostaReserva]