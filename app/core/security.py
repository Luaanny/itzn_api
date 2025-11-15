from typing import Optional, Literal

from fastapi.security import APIKeyHeader
from fastapi import Depends

from app.core.config import settings
from app.core.exceptions import unauthorized

VALID_START_HOUR = Literal[13, 14, 15, 16]

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


