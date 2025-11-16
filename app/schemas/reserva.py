from pydantic import BaseModel, EmailStr, ConfigDict, Field
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
    status: str


class AtualizarReserva(BaseModel):
    data_reserva: valid_date
    email_usuario: EmailStr
    usuario_administrador: bool = Field(default=False)


class DeletarReserva(BaseModel):
    email_usuario: EmailStr
    usuario_administrador: bool = Field(default=False)

class ListaReserva(BaseModel):
    reservas: List[RespostaReserva]
