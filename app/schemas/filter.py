from pydantic import BaseModel, EmailStr

class AgendamentoFiltro(BaseModel):
    limit: int = 10
    offset: int = 0
    autor: str | None = None

class ReservaFiltro(BaseModel):
    status: str | None = None
    limit: int = 10
    offset: int = 0
    autor: str | None = None
    