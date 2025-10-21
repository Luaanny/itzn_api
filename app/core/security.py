from typing import Annotated

import jwt
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from datetime import datetime, timedelta
from sqlalchemy import select
from app.models.user import User
from app.core.config import settings


