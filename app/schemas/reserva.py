from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import List, Literal
from app.core.annotateds import valid_date

VALID_STATUS = Literal['Aprovado', 'Negado', 'Aguardando Validação']

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
    status: VALID_STATUS
    alterado: bool


class AtualizarReserva(BaseModel):
    data_reserva: valid_date
    email_usuario: EmailStr
    justificativa: str
    usuario_administrador: bool


class AlterarStatus(BaseModel):
    status: VALID_STATUS
    email_usuario: EmailStr

class DeletarReserva(BaseModel):
    email_usuario: EmailStr
    usuario_administrador: bool

class ListaReserva(BaseModel):
    reservas: List[RespostaReserva]
