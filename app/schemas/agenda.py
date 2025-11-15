from datetime import date
from typing import List

from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr

VALID_COMPUTER_NUMBERS = Literal[2,3,4,5,6,7,8,9,10]
VALID_START_HOUR = Literal[13, 14, 15, 16]

class CriarAgenda(BaseModel):
    data_agendamento: date
    hora_inicio: VALID_START_HOUR
    numero_computador: VALID_COMPUTER_NUMBERS
    email_usuario: EmailStr
    model_config = ConfigDict(from_attributes=True)


class RespostaAgenda(BaseModel):
    id: int
    data_agendamento: date
    hora_inicio: VALID_START_HOUR
    numero_computador: VALID_COMPUTER_NUMBERS
    email_usuario: EmailStr

class AtualizarAgenda(BaseModel):
    data_agendamento: date
    hora_inicio: VALID_START_HOUR
    numero_computador: VALID_COMPUTER_NUMBERS
    email_usuario: EmailStr

class DeletarAgenda(BaseModel):
    email_usuario: EmailStr
    administrador: bool

class ListaAgenda(BaseModel):
    agendamentos: List[RespostaAgenda]