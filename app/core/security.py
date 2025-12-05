from typing import Optional
from datetime import date

from fastapi.security import APIKeyHeader
from fastapi import Depends

from app.core.config import settings
from app.core.exceptions import unauthorized

api_key_header = APIKeyHeader(
    name='X-Api-Key',
    description='API Key',
    auto_error=False
)

async def get_api_key(api_key: Optional[str] = Depends(api_key_header)):
    if not api_key:
        return unauthorized('Nenhuma API key foi fornecida no header.')

    if api_key == settings.API_KEY:
        return api_key

    return unauthorized('API key invalida.')

def data_agendamento_valido(v: date):
    if v < date.today():
        raise ValueError('Data de agendamento não pode ser no passado.')

    if v.weekday() >= 5:
        raise ValueError('Agendamentos não podem ser feitos aos Sábados e aos Domingos.')

    return v
