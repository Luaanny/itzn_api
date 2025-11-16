from datetime import date
from typing import Annotated

from pydantic import AfterValidator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_session
from app.core.security import get_api_key, data_agendamento_valido

session_type = Annotated[Session, Depends(get_session)]

check_api_key = Annotated[str, Depends(get_api_key)]

valid_date = Annotated[date, AfterValidator(data_agendamento_valido)]