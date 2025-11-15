from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_session

session_type = Annotated[Session, Depends(get_session)]