from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CriarAgenda(BaseModel):
    id: int
    data_inicio: datetime
    data_fim: datetime
    computador: int
    email_usuario: str


class PublicAgenda(BaseModel):
    data_inicio: datetime
    data_fim: datetime
    computador: int
    email_usuario: str

class ListaAgenda(BaseModel):
    agendamentos: list[PublicAgenda]