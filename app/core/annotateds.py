from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.session import get_session
from app.core.security import get_api_key

session_type = Annotated[Session, Depends(get_session)]

check_api_key = Annotated[str, Depends(get_api_key)]