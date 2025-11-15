from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from app.core.annotateds import valid_date


class CriarReserva(BaseModel):
    data_reserva: valid_date
    justificativa: str
    email_usuario: EmailStr
    model_config = ConfigDict(from_attributes=True)


class RespostaReserva(BaseModel):
    id: int
    data_reserva: valid_date
    justificativa: str
    email_usuario: EmailStr


class AtualizarReserva(BaseModel):
    data_reserva: valid_date
    email_usuario: EmailStr


class DeletarReserva(BaseModel):
    email_usuario: EmailStr
    administrador: bool

class ListaReserva(BaseModel):
    reservas: List[RespostaReserva]
